"use client";
import { useState, useEffect } from "react";
import { useParams } from "next/navigation";

const apiUrl = process.env.NEXT_PUBLIC_API_URL;

export default function ChatPage() {
    const { chat_id } = useParams(); // Get chat_id from URL
    const [messages, setMessages] = useState([]);
    const [input, setInput] = useState("");

    // ✅ Fetch chat messages on mount & refresh on new message
    useEffect(() => {
        const fetchMessages = async () => {
            try {
                const res = await fetch(`${apiUrl}/chats/${chat_id}/messages/`, { cache: "no-store" });
                if (!res.ok) throw new Error("Failed to fetch messages");
                const data = await res.json();
                setMessages(data);
            } catch (error) {
                console.error("Error fetching messages:", error);
            }
        };
        fetchMessages();
    }, [chat_id]);

    // ✅ Send message (User -> API -> Bot)
    const sendMessage = async () => {
        if (!input.trim()) return; // Prevent sending empty messages

        try {
            const res = await fetch(`${apiUrl}/messages/`, {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ chat_id: chat_id, sender: "user", text: input }),
            });

            if (!res.ok) throw new Error("Failed to send message");

            const { user_message, bot_message } = await res.json();

            // ✅ Update UI with new messages
            setMessages((prev) => [...prev, user_message, bot_message]);
            setInput(""); // Clear input field
        } catch (error) {
            console.error("Error sending message:", error);
        }
    };

    return (
        <div className="flex flex-col items-center min-h-screen p-4">
            <h1 className="text-2xl font-bold mb-4">Chat {chat_id}</h1>

            {/* ✅ Chat Box */}
            <div className="w-full max-w-lg h-[500px] overflow-y-auto border p-4 rounded-lg bg-gray-100">
                {messages.length === 0 ? (
                    <p className="text-gray-500">No messages yet.</p>
                ) : (
                    messages.map((msg) => (
                        <div
                            key={msg.id}
                            className={`p-2 my-1 rounded-lg max-w-[75%] ${
                                msg.sender === "user"
                                    ? "bg-blue-500 text-white self-end ml-auto"
                                    : "bg-gray-300 text-gray-900 self-start mr-auto"
                            }`}
                        >
                            {msg.text}
                            <br/>
                            {msg.timestamp}
                        </div>
                    ))
                )}
            </div>

            {/* ✅ Message Input */}
            <div className="flex w-full max-w-lg mt-4 gap-2">
                <input
                    type="text"
                    value={input}
                    onChange={(e) => setInput(e.target.value)}
                    placeholder="Type a message..."
                    className="flex-1 p-2 border rounded-lg text-black"
                />
                <button onClick={sendMessage} className="p-2 bg-blue-500 rounded-lg text-black">
                    Send
                </button>
            </div>
        </div>
    );
}
