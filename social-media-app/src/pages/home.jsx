import { getUser } from "../hooks/user.actions";

function Home() {
  const user = getUser();

  return (
    <div>
      <h1>Aprendiendo React</h1>
      <p>Hola Mundooo, {user.username} va con toda</p>
    </div>
  );
}
export default Home;
