import { QueryClient, QueryClientProvider } from 'react-query';
import { Link, BrowserRouter, Navigate, Routes, Route } from 'react-router-dom';
import { AuthProvider } from "./context/auth";
import { UserProvider } from "./context/user";
import { useAuth } from "./hooks";
import ChatsPage from './components/ChatsPage';
import TopNav from "./components/TopNav";
import Login from "./components/Login";
import Profile from "./components/Profile";
import Registration from "./components/Registration";
// import './App.css'

const queryClient = new QueryClient();

function NotFound() {
  return <h1>404: not found</h1>;
}

function ErrorPage() {
  return (
    <>
      <h1>an error has occurred</h1>
      <p>contact site admin for support</p>
    </>
  );
}

function Home() {
  const { isLoggedIn, logout } = useAuth();

  if (! isLoggedIn) {
    return (
      <div className="justify-self-center m-16">
        <p>chat application is a chat application</p>
        <Link className="text-violet-400" to="/login">get started</Link>
      </div>
    )
  }
  else {
    return (
      <Navigate to="/chats" />
    )
  }
}

function Header() {
  return (
    <header>
      <TopNav />
    </header>
  );
}

function AuthenticatedRoutes() {
  return (
    <Routes>
      <Route path="/" element={<Home />} />
      <Route path="/chats" element={<ChatsPage />}>
        <Route path="/chats/:ChatId" element={<ChatsPage />} />
      </Route>
      <Route path="/profile" element={<Profile />} />
      <Route path="/error/404" element={<NotFound />} />
      <Route path="*" element={<Navigate to="/chats" />} />
    </Routes>
  );
}

function UnauthenticatedRoutes() {
  return (
    <Routes>
      <Route path="/" element={<Home />} />
      <Route path="/login" element={<Login />} />
      <Route path="/registration" element={<Registration />} />
      <Route path="*" element={<Navigate to="/login" />} />
    </Routes>
  );
}

function Main() {
  const { isLoggedIn } = useAuth();

  return (
    <main className="px-4 h-fitted my-4">
      {isLoggedIn ?
        <AuthenticatedRoutes /> :
        <UnauthenticatedRoutes />
      }
    </main>
  );
}

function App() {
  const className = "h-dvh bg-zinc-800 flex flex-col mx-auto max-w-3xl"

  return (
    <QueryClientProvider client={queryClient}>
      <AuthProvider>
        <BrowserRouter>
          <UserProvider>
            <div className={className}>
              <Header />
              <Main />
            </div>
          </UserProvider>
        </BrowserRouter>
      </AuthProvider>
    </QueryClientProvider>
  );
}

export default App
