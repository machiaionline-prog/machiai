const express = require("express");
const axios = require("axios");
require("dotenv").config();

const app = express();
const PORT = process.env.PORT || 3000;

const BOT_PERSONALITY = `
You are Machi AI.
You are a funny Tamil Nadu friend from Chennai.
Reply casually in Tamil + English mix.
Be funny and friendly.
`;

app.use((req, res, next) => {
  res.setHeader("Access-Control-Allow-Origin", "*");
  res.setHeader("Access-Control-Allow-Methods", "GET, POST, OPTIONS");
  res.setHeader("Access-Control-Allow-Headers", "Content-Type, Authorization");

  if (req.method === "OPTIONS") {
    return res.sendStatus(200);
  }

  next();
});

app.use(express.json());

app.get("/", (req, res) => {
  res.send("Machi AI is running");
});

app.get("/webhook", (req, res) => {
  const VERIFY_TOKEN = process.env.VERIFY_TOKEN || "machiai";

  const mode = req.query["hub.mode"];
  const token = req.query["hub.verify_token"];
  const challenge = req.query["hub.challenge"];

  if (mode && token === VERIFY_TOKEN) {
    console.log("Webhook verified!");
    return res.status(200).send(challenge);
  }

  return res.sendStatus(403);
});

async function getMachiReply(userMessage) {
  const response = await axios.post(
    "https://api.openai.com/v1/chat/completions",
    {
      model: "gpt-4o-mini",
      messages: [
        {
          role: "system",
          content: BOT_PERSONALITY.trim()
        },
        {
          role: "user",
          content: userMessage
        }
      ]
    },
    {
      headers: {
        Authorization: `Bearer ${process.env.OPENAI_API_KEY}`,
        "Content-Type": "application/json"
      }
    }
  );

  return response.data.choices[0].message.content;
}

async function sendWhatsAppMessage(text, to) {
  if (!process.env.WHATSAPP_PHONE_ID) {
    throw new Error("WHATSAPP_PHONE_ID is missing");
  }

  if (!process.env.WHATSAPP_ACCESS_TOKEN) {
    throw new Error("WHATSAPP_ACCESS_TOKEN is missing");
  }

  await axios.post(
    `https://graph.facebook.com/v18.0/${process.env.WHATSAPP_PHONE_ID}/messages`,
    {
      messaging_product: "whatsapp",
      to,
      text: { body: text }
    },
    {
      headers: {
        Authorization: `Bearer ${process.env.WHATSAPP_ACCESS_TOKEN}`,
        "Content-Type": "application/json"
      }
    }
  );
}

async function handleChat(req, res) {
  console.log("Request:", req.body);

  const userMessage = req.body?.message;

  if (!process.env.OPENAI_API_KEY) {
    return res.status(500).json({ error: "OPENAI_API_KEY is missing" });
  }

  if (!userMessage || typeof userMessage !== "string") {
    return res.status(400).json({ error: "message must be a non-empty string" });
  }

  try {
    const reply = await getMachiReply(userMessage);
    return res.json({ status: "ok", reply });
  } catch (err) {
    console.log(err.response?.data || err.message);
    return res.status(500).json({ error: "Failed to get AI reply" });
  }
}

async function handleWebhook(req, res) {
  console.log("Webhook payload:", JSON.stringify(req.body));

  const incomingMessage = req.body?.entry?.[0]?.changes?.[0]?.value?.messages?.[0];
  const userMessage = incomingMessage?.text?.body;
  const from = incomingMessage?.from;

  if (!incomingMessage) {
    return res.json({ status: "ignored" });
  }

  if (!process.env.OPENAI_API_KEY) {
    return res.status(500).json({ error: "OPENAI_API_KEY is missing" });
  }

  try {
    const reply = await getMachiReply(userMessage);
    await sendWhatsAppMessage(reply, from);
    return res.json({ status: "ok" });
  } catch (err) {
    console.log(err.response?.data || err.message);
    return res.status(500).json({ error: "Failed to process webhook" });
  }
}

app.post("/chat", handleChat);
app.post("/webhook", handleWebhook);

app.listen(PORT, () => {
  console.log(`Server running on port ${PORT}`);
});
