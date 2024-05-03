import { useApi, useAuth } from "../hooks";
import { useState } from "react";
import { useMutation, useQueryClient } from "react-query";
import { useNavigate, useParams } from "react-router-dom";
import Button from "./Button";
import FormInput from "./FormInput";


function MessageForm({ chat }) {
  const api = useApi();
  const queryClient = useQueryClient();
  const navigate = useNavigate();
  const { token } = useAuth();
  const [text, setText] = useState("");

  const { ChatId } = useParams();
  const url = "/chats/" + ChatId + "/messages"

  const mutation = useMutation({
    mutationFn: () => (
      api.post(
        url,
        {
          text
        },
      ).then((response) => response.json())
    ),
    onSuccess: (data) => {
      queryClient.invalidateQueries({
        queryKey: ["messages"],
      });
    },
  });

  const onSubmit = (e) => {
    e.preventDefault();
    mutation.mutate();
    e.target.reset();
  };

  return (
    <div className="py-1 border-2 border-violet-400 rounded mb-4">
      <form className="grid grid-cols-5 grid-rows-1 gap-x-5 justify-between px-2 py-2" onSubmit={onSubmit}>
        <div className="col-span-4">
          <FormInput className="w-full" type="text" setter={setText}/>
        </div>
        <Button className="col-span-1" type="submit">send</Button>
      </form>
    </div>
  )
}

export default MessageForm