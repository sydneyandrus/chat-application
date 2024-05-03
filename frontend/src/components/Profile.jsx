import { useEffect, useState } from "react";
import { useAuth, useUser } from "../hooks";
import Button from "./Button";
import FormInput from "./FormInput";

function Profile() {
  const { logout } = useAuth();
  const user = useUser();

  return (
    <div className="max-w-96 mx-auto px-4 py-8">
      <h2 className="text-2xl font-bold py-2 text-blue-400">
        details
      </h2>
      <div className="border rounded px-4 py-2">
        <p><span className="text-green-400">username:</span> &ensp;{user?.username}</p>
        <br></br>
        <p><span className="text-green-400">email:</span> &ensp;{user?.email}</p>
        <br></br>
        <p><span className="text-green-400">member since:</span> &ensp;<time>{new Date(user?.created_at).toDateString()}</time> </p>
      </div>
      <Button className="my-4" onClick={logout}>
        logout
      </Button>
    </div>
  );
}

export default Profile;