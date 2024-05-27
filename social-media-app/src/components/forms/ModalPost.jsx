import { Button,Modal, Form } from "react-bootstrap";
import { PropTypes } from "prop-types";

function ModalPost({ show, handleClose, form, setForm, validated, handleSubmit }) {
  return (
    <Modal show={show} onHide={handleClose}>
      <Modal.Header closeButton className="border-0">
        <Modal.Title>Create Post</Modal.Title>
      </Modal.Header>
      <Modal.Body className="border-0">
        <Form noValidate validated={validated} onSubmit={handleSubmit}>
          <Form.Group className="mb-3">
            <Form.Control
              name="body"
              value={"body" in form ? form.body : ""}
              onChange={(e) => setForm({ ...form, body: e.target.value })}
              as="textarea"
              rows={3}
            />
          </Form.Group>
        </Form>
      </Modal.Body>
      <Modal.Footer>
        <Button
          variant="primary"
          onClick={handleSubmit}
          disabled={form.body === ""}
        >
          Post
        </Button>
      </Modal.Footer>
    </Modal>
  );
}

ModalPost.propTypes = {
  show: PropTypes.bool.isRequired,
  handleClose: PropTypes.func.isRequired,
  form: PropTypes.object.isRequired,
  setForm: PropTypes.func.isRequired,
  validated: PropTypes.bool.isRequired,
  handleSubmit: PropTypes.func.isRequired,
}

export default ModalPost;