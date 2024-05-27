import React, { useState } from "react";
import { PropTypes } from "prop-types";
import { format } from "timeago.js";
import {
  LikeFilled,
  CommentOutlined,
  LikeOutlined,
  MoreOutlined,
} from "@ant-design/icons";
import { Image, Card, Button, Modal, Form, Dropdown } from "react-bootstrap";
import { randomAvatar } from "../../utils";
import axiosService from "../../helpers/axios";
import Toaster from "../Toaster";
import { getUser } from "../../hooks/user.actions";

const MoreToggleIcon = React.forwardRef(({ onClick }, ref) => (
  <a
    href="#"
    ref={ref}
    onClick={(e) => {
      e.preventDefault();
      onClick(e);
    }}
  >
    <MoreOutlined />
  </a>
));

MoreToggleIcon.propTypes = {
  onClick: PropTypes.func,
};

MoreToggleIcon.displayName = "MoreToggleIcon"; // nombre de visualización

const UpdatePost = ({ post }) => {
  const handleClick = (e) => {
    e.preventDefault();
    console.log("Update post", post.body);
  }
  return (<Dropdown.Item onClick={handleClick}>Update</Dropdown.Item>)
}

UpdatePost.propTypes = {
  post: PropTypes.object.isRequired,
}

function Post(props) {
  const { post, refresh } = props;
  const [showToast, setShowToast] = useState(false);
  const user = getUser();

  const handleDelete = () => {
    axiosService
      .delete(`/post/${post.id}/`)
      .then(() => {
        setShowToast(true);
        refresh();
      })
      .catch((err) => console.error(err.response.data));
  };

  const handleLikeClick = (action) => {
    axiosService
      .post(`/post/${post.id}/${action}/`)
      .then(() => {
        refresh();
      })
      .catch((err) => console.error(err));
  };

  return (
    <>
      <Card className="rounded-3 my-4">
        <Card.Body>
          <Card.Title className="d-flex flex-row justify-content-between">
            <div className="d-flex flex-row">
              <Image
                src={randomAvatar()}
                roundedCircle
                width={48}
                height={48}
                className="me-2 border border-primary border-2"
              />
              <div className="d-flex flex-column justify-content-start align-self-center mt-2">
                <p className="fs-6 m-0">{post.author.name}</p>
                <p className="fs-6 fw-lighter">
                  <small>{format(post.created)}</small>
                </p>
              </div>
            </div>
            {user.id !== post.author.id && ( // solo el autor del post puede eliminarlo
              <div>
                <Dropdown>
                  <Dropdown.Toggle as={MoreToggleIcon}></Dropdown.Toggle>
                  <Dropdown.Menu>
                    <UpdatePost post={post} />
                    <Dropdown.Item
                      onClick={handleDelete}
                      className="text-danger"
                    >
                      Delete
                    </Dropdown.Item>
                  </Dropdown.Menu>
                </Dropdown>
              </div>
            )}
          </Card.Title>
          <Card.Text>{post.body}</Card.Text>
          <div className="d-flex flex-row">
            <LikeFilled
              style={{
                color: "#fff",
                backgroundColor: "#0D6EFD",
                borderRadius: "50%",
                width: "18px",
                height: "18px",
                fontSize: "75%",
                padding: "2px",
                margin: "3px",
              }}
            />
            <p className="ms-1 fs-6">
              <small>{post.likes_count} like</small>
            </p>
          </div>
        </Card.Body>
        <Card.Footer className="d-flex bg-white w-50 justify-content-between border-0">
          <div className="d-flex flex-row">
            <LikeOutlined
              style={{
                width: "24px",
                height: "24px",
                padding: "2px",
                fontSize: "20px",
                color: post.liked ? "#0D6EFD" : "#C4C4C4", // Cambiar color del icono si el post está likeado
              }}
              onClick={() => {
                if (post.liked) {
                  handleLikeClick("remove_like");
                } else {
                  handleLikeClick("like");
                }
              }}
            />
            <p className="ms-1">
              <small>Like</small>
            </p>
          </div>
          <div className="d-flex flex-row">
            <CommentOutlined
              style={{
                width: "24px",
                height: "24px",
                padding: "2px",

                fontSize: "20px",
                color: "#C4C4C4",
              }}
            />
            <p className="ms-1 mb-0">
              <small>Comment</small>
            </p>
          </div>
        </Card.Footer>
      </Card>
      <Toaster
        title="Post!"
        message="Post deleted"
        type="danger"
        showToast={showToast}
        onClose={() => setShowToast(false)}
      />
    </>
  );
}

Post.propTypes = {
  post: PropTypes.object,
  refresh: PropTypes.func,
};

export default Post;
