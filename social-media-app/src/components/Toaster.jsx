import { Toast, ToastContainer } from "react-bootstrap";
import PropTypes from "prop-types"; // Importar PropTypes
function Toaster(props) {
  const { showToast, title, message, onClose, type } = props;
  return (
    <ToastContainer position="top-center">
      <Toast onClose={onClose} show={showToast} delay={3000} autohide bg={type}>
        <Toast.Header>
          <strong className="me-auto">{title}</strong>
        </Toast.Header>
        <Toast.Body>
          <p className="text-white">{message}</p>
        </Toast.Body>
      </Toast>
    </ToastContainer>
  );
}

Toaster.propTypes = { // defino los props que recibe el componente
  showToast: PropTypes.bool, // showToast es un booleano
  title: PropTypes.string, // title es un string
  message: PropTypes.string, // message es un string
  onClose: PropTypes.func, // onClose es una función
  type: PropTypes.string, // success, danger, warning, info
};

export default Toaster;