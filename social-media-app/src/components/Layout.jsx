import PropTypes from "prop-types"; // Importar PropTypes

import Navigationbar from "./Navbar";

function Layout({ children }) { // creo el componente Layout que recibe la propiedad children, sera el nodo principal
  return (
    <>
      <Navigationbar /> {/* Agrego el componente Navigationbar que será la barra de navegación */}
      <div className="container m-5">{children}</div> {/* Agrego el contenedor principal  */}
    </>
  );
}

Layout.propTypes = { // Especifico los props que recibe el componente
  children: PropTypes.node.isRequired, // Agrego la propiedad children que sea un nodo requerido
};

export default Layout;

