import { Navigate } from "react-router-dom";
import PropTypes from 'prop-types';
import { getUser } from "../hooks/user.actions";

function ProtectedRoute({ children }) {
  // obtengo el usuario
  const user = getUser();
  // si el usuario existe, se renderiza el children, si no, se redirige a la página de inicio de sesión
  return user ? <>{children}</> : <Navigate to="/login/" />;
}

// Definición de propTypes
ProtectedRoute.propTypes = {
  children: PropTypes.node.isRequired, // le indico que children es requerido
};

export default ProtectedRoute;
