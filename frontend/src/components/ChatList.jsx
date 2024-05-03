// import { useQuery } from "react-query";
import { Link, Navigate, useNavigate, useParams } from "react-router-dom";

function ChatCard({ chat, active }) {
  const className=[
    "flex flex-col",
    "border-2 rounded",
    "mb-4 p-2",
    "hover:bg-zinc-900",
    active ? 
      "bg-zinc-900 border-blue-400":
      "border-green-500",
  ].join(" ");
  return (
    <Link className={className} to={`/chats/${chat.id}`}>
      <div className="text-blue-400 font-extrabold">{chat.name}</div>
    </Link>
  );
}

function ChatList({ chats}) {
  const { ChatId } = useParams();
  const active = (chat) => chat.id === parseInt(ChatId);
  return (
    <div className="flex flex-col max-h-fitted overflow-y-scroll">
      <h3 className="py-1 border-2 border-white rounded text-center font-bold mb-4">chat list</h3>
      <div className="chat-list">
        {chats.map((chat) => (
          <ChatCard key={chat.id} chat={chat} active={active(chat)}/>
        ))}
      </div>
    </div>
  );
}

export default ChatList;