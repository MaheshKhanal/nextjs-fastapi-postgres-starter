"use client";
import React from "react";
import { apiUrl } from "../app/helpers";
import { useRouter } from "next/navigation";

function NewChatBtn({ user_id }) {

  const router = useRouter();
  
    const handleClick = async () => {
        try {
            const res = await fetch(`${apiUrl}/chats/`, {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                },
                body: JSON.stringify({ user_id: 1 }) 
            });
    
            if (!res.ok) {
                throw new Error(`HTTP error! Status: ${res.status}`);
            }
    
            const content = await res.json();
            if (content && content.chat_id) {
              router.push(`/chats/${content.chat_id}`);
          }
        } catch (error) {
            console.error("Error starting chat:", error);
        }
    };
    

  return (
    <button
      type="button"
        className="bg-green-400 text-white px-4 py-2 rounded-lg m-2 shadow-md hover:bg-blue-600 transition"
      onClick={() => handleClick()}
    >
      Start a new chat
    </button>
  );
}

export default NewChatBtn;
