import { NavLink } from "react-router-dom";
import { useAuth, useUser } from "../hooks";

function NavItem({ to, name, right }) {
  const className = [
    "text-center font-bold mx-4",
    "py-2 px-4",
    "hover:text-green-400",
    right ? "border-0" : "border-0"
  ].join(" ")

  const getClassName = ({ isActive }) => (
    isActive ? className + " text-blue-400" : className
  );

  return (
    <NavLink to={to} className={getClassName}>
      {name}
    </NavLink>
  );
}

function AuthenticatedNavItems() {
  const user = useUser();

  return (
    <>
      <NavItem to="/" name="pony express" />
      <div className="flex-1" />
      <NavItem to="/profile" name={user?.username} right />
    </>
  );
}

function UnauthenticatedNavItems() {
  return (
    <>
      <NavItem to="/" name="pony express" />
      <div className="flex-1" />
      <NavItem to="/login" name="login" right />
    </>
  );
}


function TopNav() {
  const { isLoggedIn } = useAuth();

  return (
    <nav className="flex flex-row border-2 border-violet-400 rounded mt-4 mx-4">
      {isLoggedIn ?
        <AuthenticatedNavItems /> :
        <UnauthenticatedNavItems />
      }
    </nav>
  );
}

export default TopNav;