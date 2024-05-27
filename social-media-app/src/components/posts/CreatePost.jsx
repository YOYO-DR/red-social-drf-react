import { Button, Modal, Form } from "react-bootstrap";
import axiosService from "../../helpers/axios";
import { getUser } from "../../hooks/user.actions";
import { useState } from "react";
import Toaster from "../Toaster";
import { PropTypes } from "prop-types";
import ModalPost from "../forms/ModalPost";

function CreatePost(props) {
  const {changePost} = props;
  const formBase = { body: "" };
  const [show, setShow] = useState(false); // inicializo el estado del modal
  const handleClose = () => setShow(false); // función para cerrar el modal
  const handleShow = () => setShow(true); // función para abrir el modal
  const [validated, setValidated] = useState(false); // inicializo el estado de validación
  const [form, setForm] = useState(formBase);
  const user = getUser();
  const [showToast, setShowToast] = useState(false);
  const [toastMessage, setToastMessage] = useState("");
  const [toastType, setToastType] = useState("");

  const handleSubmit = (event) => {
    event.preventDefault();
    const createPostForm = event.currentTarget;
    if (createPostForm.checkValidity() === false) {
      // valido el formulario
      event.stopPropagation();
      setValidated(true); // muestro los mensajes de error
      return;
    }

    const data = {
      author: user.id, // obtengo el id del usuario
      body: form.body, // obtengo el cuerpo del post
    };

    axiosService // envío la petición POST al backend, con axiosService porque necesito enviar el token de autenticación
      .post("/post/", data)
      .then(() => {
        handleClose();
        setToastMessage("Post created 🚀");
        setToastType("success");
        setForm(formBase);
        setShowToast(true);
        changePost(); // actualizar los posts
      })
      .catch((error) => {
        setToastMessage("An error occurred.");
        setToastType("danger");
        console.log(error.response.data)
      });
  };

  return (
    <>
      <Form.Group className="my-3 w-75">
        <Form.Control
          className="py-2 rounded-pill border-primary
  text-primary"
          type="text"
          placeholder="Write a post"
          onClick={handleShow}
        />
      </Form.Group>
      <ModalPost show={show} handleClose={handleClose} form={form} setForm={setForm} validated={validated} handleSubmit={handleSubmit} />

      <Toaster
        title="Post!"
        message={toastMessage}
        showToast={showToast}
        type={toastType}
        onClose={() => setShowToast(false)}
      />
    </>
  );
}

CreatePost.propTypes = {
  changePost: PropTypes.func.isRequired,
};
export default CreatePost;
