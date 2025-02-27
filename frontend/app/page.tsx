import Image from "next/image";
import Chatbox from "../components/chatbox";
import NewChatBtn from "../components/newchatBtn";
import ExistingChatBtn from "@/components/existingChatBtn";

type User = {
  id: string;
  name: string;
};

const apiUrl = process.env.NEXT_PUBLIC_API_URL;

export default async function Home() {
  console.log("fetch", `${apiUrl}/users/me`);
  const user: User = await fetch(`${apiUrl}/users/me`).then((res) =>
    res.json()
  );

  const chats = await fetch(`${apiUrl}/users/${user.id}/chats/`, {
    cache: "no-cache",
  })
    .then((res) => res.json())
    .catch((err) => {
      console.error("Something is wrong");
    });

  return (
    <main className="flex min-h-screen flex-col items-center p-24">
      Hello, {user.name}
      {<NewChatBtn user_id={user.id} />}
      <div>Existing Chat threads</div>
      {chats && chats.length > 0 ? (
        chats.map((item) => <ExistingChatBtn item={item} />)
      ) : (
        <p>You dont have any existing threads...</p>
      )}
    </main>
  );
}
