import React, { useState } from "react";
import { Form, Button } from "react-bootstrap";
import axios from "axios";
import { useNavigate } from "react-router-dom";

function RegistrationForm() {
  const navigate = useNavigate(); // hook de react-router-dom para navegar entre rutas
  const [validated, setValidated] = useState(false);
  const [form, setForm] = useState({});
  const [error, setError] = useState(null);

  const handleSubmit = (event) => {
    event.preventDefault();
    const registrationForm = event.currentTarget;
    if (registrationForm.checkValidity() === false) {
      event.stopPropagation();
    }
    setValidated(true);
    const data = {
      username: form.username,
      password: form.password,
      email: form.email,
      first_name: form.first_name,
      last_name: form.last_name,
      bio: form.bio,
    };
    
    axios
      .post("http://localhost:8000/api/auth/register/", data)
      .then((res) => {
        // Registering the account and tokens in the
        // store
        localStorage.setItem(
          "auth",
          JSON.stringify({
            access: res.data.access,
            refresh: res.data.refresh,
            user: res.data.user,
          })
        );

        navigate("/");
      })
      .catch((err) => {
        if (err.message) {
          setError(err.request.response);
        }
      });
  };
}
