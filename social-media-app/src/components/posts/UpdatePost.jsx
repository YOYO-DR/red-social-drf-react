import { Dropdown } from "react-bootstrap";
import axiosService from "../../helpers/axios";
import { useState } from "react";
import { PropTypes } from "prop-types";
import ModalPost from "../forms/ModalPost";

const UpdatePost = ({
  post,
  changePost,
  setShowToast,
  setToastMessage,
  setToastType,
}) => {
  const formBase = { body: "" }; // inicializo el estado del formulario, con los campos que tendra para no tener problemas si un valor se encuentra vacío
  const [show, setShow] = useState(false); // inicializo el estado del modal
  const handleClose = () => setShow(false); // función para cerrar el modal
  const handleShow = () => setShow(true); // función para abrir el modal
  const [validated, setValidated] = useState(false); // inicializo el estado de validación
  const [form, setForm] = useState({ body: post.body });

  const handleSubmit = (event) => {
    event.preventDefault();
    const UpdatePostForm = event.currentTarget;
    if (UpdatePostForm.checkValidity() === false) {
      // valido el formulario
      event.stopPropagation();
      setValidated(true); // muestro los mensajes de error
      return;
    }

    axiosService // envío la petición PUT al backend, con axiosService porque necesito enviar el token de autenticación
      .put(`/post/${post.id}/`, form)
      .then(() => {
        handleClose();
        setToastMessage("Post update 🚀");
        setToastType("success");
        setForm(formBase);
        setShowToast(true);
        changePost(); // actualizar los posts
      })
      .catch((error) => {
        setToastMessage("An error occurred.");
        setToastType("danger");
        console.log(error.response.data);
      });
  };

  const handleClick = (e) => {
    e.preventDefault();

    // obtengo el post
    const data = {
      post: post.id, // obtengo el id del post
      author: post.author.id, // obtengo el id del usuario del post
    };

    axiosService.get(`/post/${post.id}/`, data).then((res) => {
      const post = res.data;
      console.log(post);
      setForm({
        body: post.body,
        post: post.id,
        author: post.author.id,
      }); // actualizo el estado del formulario con el valor del post
      handleShow();
    });
  };
  return (
    <>
      <Dropdown.Item onClick={handleClick}>Update</Dropdown.Item>
      <ModalPost
        show={show}
        handleClose={handleClose}
        form={form}
        setForm={setForm}
        validated={validated}
        handleSubmit={handleSubmit}
      />
    </>
  );
};

UpdatePost.propTypes = {
  post: PropTypes.object.isRequired,
  changePost: PropTypes.func.isRequired,
  setShowToast: PropTypes.func.isRequired,
  setToastMessage: PropTypes.func.isRequired,
  setToastType: PropTypes.func.isRequired,
};

export default UpdatePost;
