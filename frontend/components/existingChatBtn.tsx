'use client'
import React from 'react'
import { useRouter } from "next/navigation";

function ExistingChatBtn({item}) {
    console.log("ITEM : ", item)
    const router = useRouter(); 
  return (
    <div>
       <button
            key={item.chat_id}
            className="bg-blue-500 text-white px-4 py-2 rounded-lg m-2 shadow-md hover:bg-blue-600 transition"
            onClick={()=>router.push(`/chats/${item.chat_id}`)}
          >
            Chat {item.chat_id} created {new Date(item.created_at).toLocaleDateString()}
          </button>
    </div>
  )
}

export default ExistingChatBtn
