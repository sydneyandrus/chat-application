function Button(props) {
  const className = [
    props.className || "",
    "border rounded",
    "px-4 py-2",
    props.disabled ?
      "bg-zinc-600 italic" :
      "border-lgrn bg-transparent hover:bg-zinc-900",
  ].join(" ");

  return (
    <button {...props} className={className}>
      {props.children}
    </button>
  );
}

export default Button;