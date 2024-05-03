import { useQuery } from "react-query";
import { Link, Navigate, useNavigate, useParams } from "react-router-dom";

import Chat from './Chat';
import ChatList from './ChatList'
import MessageForm from './MessageForm'
// import "./ChatsPage.css";



function EmptyChatPage() {
  return (
    <div className="col-span-2">
      <p>loading chats</p>
    </div>
  )
}

function ChatWrapper() {
  const { ChatId } = useParams();

  if (!ChatId) {
    return (<>
      <Chat chat={{}} />
    </>);
  }

  const navigate = useNavigate();
  const { data, isLoading } = useQuery({
    queryKey: ["chats", ChatId],
    queryFn: () => (
      fetch(`http://127.0.0.1:8000/chats/${ChatId}`)
        .then((response) => {
          if (!response.ok) {
            response.status === 404 ?
              navigate("/error/404") :
              navigate("/error");
          }
          return response.json()
        })
    ),
  });

  if (isLoading) {
    return (<>
      <p>is loading</p>
      <Chat chat={{}} />
    </>);
  }

  if (data?.chat) {
    return (<div className="col-span-2 flex flex-col max-h-fitted">
      <h3 className="py-1 border-2 border-white rounded text-center font-bold mb-4">{data.chat.name || "name of chat"}</h3>
      <Chat chat={data.chat} />
      <MessageForm chat={data.chat} />
    </div>);
  }

  return <Navigate to="/error" />;
}

function ChatsPage() {
  const {chatId} = useParams();

  const navigate = useNavigate();
  const { data, isLoading, error } = useQuery({
    queryKey: ["chats"],
    queryFn: () => (
      fetch("http://127.0.0.1:8000/chats")
        .then((response) => {
          if (!response.ok) {
            response.status === 404 ?
              navigate("/error/404") :
              navigate("/error");
          }
          return response.json()
        })
    ),
  });

  if (error) {
    return <Navigate to="/error" />
  }

  return (
    <div className="h-max grid grid-cols-3 gap-5">
      {!isLoading && data?.chats ?
        <ChatList chats={data.chats} /> :
        <EmptyChatPage />
      }
      <ChatWrapper />
    </div>
  );
}

export default ChatsPage;