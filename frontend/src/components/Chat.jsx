import { useQuery } from "react-query";
import { Link, Navigate, useNavigate, useParams } from "react-router-dom";
import ScrollContainer from "./ScrollContainer";


function MessageCard({ message }) {
  return (
    <div className="border border-violet-400 rounded m-2 p-2">
      <div className="flex flex-row justify-between">
        <div className="text-green-500 text-sm font-bold">{message.user.username || "sender"}</div>
        <div className="text-gray-400 text-xs"><time>{new Date(message.created_at).toDateString()} - {new Date(message.created_at).toLocaleTimeString()}</time></div>
      </div>
      <div className="message-card-text">{message.text || "message text"}</div>
    </div>
  );
}

function Chat({ chat }) {
  if (!chat?.name) {
    return (
      <div className="flex flex-col col-span-2 border-2 border-blue-400 rounded p-16 h-chat">
        <p>select a chat</p>
      </div>
    );
  }

  const { ChatId } = useParams();

  const navigate = useNavigate();
  const { data, isLoading, error } = useQuery({
    queryKey: ["messages", ChatId],
    queryFn: () => (
      fetch(`http://127.0.0.1:8000/chats/${ChatId}/messages`)
        .then((response) => {
          response.clone
          if (!response.ok) {
            response.status === 404 ?
              navigate("/error/404") :
              navigate("/error");
          }
          return response.json()
        })
    )},
  );

  if (isLoading) {
    return (<>
      <p>is loading</p>
    </>);
  }

  if (error) {
    return <p>error</p>
  }

  return (
    <div className="flex flex-col border-2 border-blue-400 rounded overflow-y-scroll mb-4">
      <ScrollContainer
      children={data.messages.map((message) => (
        <MessageCard key={message.id} message={message} />
      ))}
      />
    </div>
  );
}

export default Chat;
