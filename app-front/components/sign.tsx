"use client";

import React, { useState, useEffect } from "react";
import { Button, Input, Checkbox, Link, Form } from "@heroui/react";
import { Icon } from "@iconify/react";
import {
  Modal,
  ModalContent,
  ModalHeader,
  ModalBody,
  useDisclosure,
} from "@heroui/modal";
import { Divider } from "@heroui/divider";
import {
  Dropdown,
  DropdownTrigger,
  DropdownMenu,
  DropdownSection,
  DropdownItem,
} from "@heroui/dropdown";

export default function Sign() {
  const { isOpen, onOpen, onOpenChange } = useDisclosure();
  const [isVisible, setIsVisible] = useState(false);
  const [isConfirmVisible, setIsConfirmVisible] = useState(false);

  // Estados para los datos de "Sign Up"
  const [signUpData, setSignUpData] = useState({
    name: "",
    username: "",
    email: "",
    password: "",
    confirmPassword: "",
  });

  // Estados para los datos de "Log In"
  const [logInData, setLogInData] = useState({
    username: "",
    password: "",
  });

  // Estado para almacenar el nombre del usuario que inició sesión
  const [loggedInUser, setLoggedInUser] = useState<string | null>(null);

  // Verificar si hay un token al cargar la aplicación
  useEffect(() => {
    const token = localStorage.getItem("authToken");
    if (token) {
      // Opcional: Decodificar el token para obtener información del usuario
      // Aquí asumimos que el servidor tiene un endpoint para validar el token
      fetch("http://localhost:8000/validate-token", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${token}`,
        },
      })
        .then((response) => {
          if (!response.ok) {
            throw new Error("Failed to validate token");
          }
          return response.json();
        })
        .then((data) => {
          setLoggedInUser(data.name); // Restaurar el nombre del usuario
        })
        .catch((error) => {
          console.error("Error validating token:", error);
          localStorage.removeItem("authToken"); // Eliminar token inválido
        });
    }
  }, []);

  // Manejar cambios en los campos de "Sign Up"
  const handleSignUpChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const { name, value } = e.target;
    setSignUpData((prev) => ({ ...prev, [name]: value }));
  };

  // Manejar cambios en los campos de "Log In"
  const handleLogInChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const { name, value } = e.target;
    setLogInData((prev) => ({ ...prev, [name]: value }));
  };

  // Manejar envío del formulario de "Sign Up"
  const handleSignUpSubmit = async (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    if (signUpData.password !== signUpData.confirmPassword) {
      alert("Passwords do not match!");
      return;
    }

    try {
      const response = await fetch("http://localhost:8000/user", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          name: signUpData.name,
          username: signUpData.username,
          email: signUpData.email,
          password: signUpData.password,
        }),
      });

      if (!response.ok) {
        throw new Error("Failed to register");
      }

      const data = await response.json();
      console.log("Registration successful:", data);
      alert("Registration successful!");
    } catch (error) {
      console.error("Error during registration:", error);
      alert("Registration failed. Please try again.");
    }
  };

  // Manejar envío del formulario de "Log In"
  const handleLogInSubmit = async (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault();

    try {
      const body = new URLSearchParams({
        username: logInData.username,
        password: logInData.password,
      });

      const response = await fetch("http://localhost:8000/login", {
        method: "POST",
        headers: {
          "Content-Type": "application/x-www-form-urlencoded",
        },
        body: body.toString(),
      });

      if (!response.ok) {
        throw new Error("Failed to log in");
      }

      const data = await response.json();
      console.log("Login successful:", data);

      // Guardar el token en localStorage
      localStorage.setItem("authToken", data.token);

      // Guardar el nombre del usuario en el estado
      setLoggedInUser(data.name);

      alert(`Welcome, ${data.name}!`);
    } catch (error) {
      console.error("Error during login:", error);
      alert("Login failed. Please check your credentials and try again.");
    }
  };

  const handleLogOut = () => {
    localStorage.removeItem("authToken");
    setLoggedInUser(null);
    alert("You have been logged out.");
  };

  const toggleVisibility = () => setIsVisible(!isVisible);
  const toggleConfirmVisibility = () => setIsConfirmVisible(!isConfirmVisible);

  return (
    <>
      {/* Mostrar el nombre del usuario o el botón "Sign Up" */}
      {loggedInUser ? (
        <Dropdown>
          <DropdownTrigger>
            <Button color="primary">{loggedInUser}</Button>
          </DropdownTrigger>
          <DropdownMenu>
            <DropdownSection>
              <DropdownItem key="profile">Profile</DropdownItem>
              <DropdownItem key="settings">Settings</DropdownItem>
              <DropdownItem
                key="logout"
                className="text-danger"
                color="danger"
                onClick={handleLogOut}
              >
                Log Out
              </DropdownItem>
            </DropdownSection>
          </DropdownMenu>
        </Dropdown>
      ) : (
        <Button onPress={onOpen}>Sign Up</Button>
      )}
      <Modal isOpen={isOpen} onOpenChange={onOpenChange} size="2xl" backdrop="blur">
        <ModalContent>
          <ModalHeader>Sign Up & Log In</ModalHeader>
          <ModalBody>
            <div className="flex h-full w-full items-center justify-center">
              <div className="flex w-full max-w-2xl flex-row gap-8 rounded-large px-8 pb-10 pt-6">
                {/* Sign Up Form */}
                <div className="flex w-1/2 flex-col gap-4">
                  <p className="pb-4 text-left text-3xl font-semibold">
                    Sign Up
                    <span aria-label="emoji" className="ml-2" role="img">
                      👋
                    </span>
                  </p>
                  <form
                    className="flex flex-col gap-4"
                    onSubmit={handleSignUpSubmit}
                  >
                    <Input
                      isRequired
                      label="Name"
                      labelPlacement="outside"
                      name="name"
                      placeholder="Enter your name"
                      type="text"
                      variant="bordered"
                      value={signUpData.name}
                      onChange={handleSignUpChange}
                    />
                    <Input
                      isRequired
                      label="Username"
                      labelPlacement="outside"
                      name="username"
                      placeholder="Enter your username"
                      type="text"
                      variant="bordered"
                      value={signUpData.username}
                      onChange={handleSignUpChange}
                    />
                    <Input
                      isRequired
                      label="Email"
                      labelPlacement="outside"
                      name="email"
                      placeholder="Enter your email"
                      type="email"
                      variant="bordered"
                      value={signUpData.email}
                      onChange={handleSignUpChange}
                    />
                    <Input
                      isRequired
                      endContent={
                        <button type="button" onClick={toggleVisibility}>
                          {isVisible ? (
                            <Icon
                              className="pointer-events-none text-2xl text-default-400"
                              icon="solar:eye-closed-linear"
                            />
                          ) : (
                            <Icon
                              className="pointer-events-none text-2xl text-default-400"
                              icon="solar:eye-bold"
                            />
                          )}
                        </button>
                      }
                      label="Password"
                      labelPlacement="outside"
                      name="password"
                      placeholder="Enter your password"
                      type={isVisible ? "text" : "password"}
                      variant="bordered"
                      value={signUpData.password}
                      onChange={handleSignUpChange}
                    />
                    <Input
                      isRequired
                      endContent={
                        <button type="button" onClick={toggleConfirmVisibility}>
                          {isConfirmVisible ? (
                            <Icon
                              className="pointer-events-none text-2xl text-default-400"
                              icon="solar:eye-closed-linear"
                            />
                          ) : (
                            <Icon
                              className="pointer-events-none text-2xl text-default-400"
                              icon="solar:eye-bold"
                            />
                          )}
                        </button>
                      }
                      label="Confirm Password"
                      labelPlacement="outside"
                      name="confirmPassword"
                      placeholder="Confirm your password"
                      type={isConfirmVisible ? "text" : "password"}
                      variant="bordered"
                      value={signUpData.confirmPassword}
                      onChange={handleSignUpChange}
                    />
                    <Checkbox isRequired className="py-4" size="sm">
                      I agree with the&nbsp;
                      <Link className="relative z-[1]" href="#" size="sm">
                        Terms
                      </Link>
                      &nbsp; and&nbsp;
                      <Link className="relative z-[1]" href="#" size="sm">
                        Privacy Policy
                      </Link>
                    </Checkbox>
                    <Button color="primary" type="submit">
                      Sign Up
                    </Button>
                  </form>
                </div>

                <Divider orientation="vertical" />

                {/* Log In Form */}
                <div className="flex w-1/2 flex-col gap-4">
                  <p className="pb-4 text-left text-3xl font-semibold">
                    Log In
                    <span aria-label="emoji" className="ml-2" role="img">
                      👋
                    </span>
                  </p>
                  <Form
                    className="flex flex-col gap-4"
                    validationBehavior="native"
                    onSubmit={handleLogInSubmit}
                  >
                    <Input
                      isRequired
                      label="Username"
                      labelPlacement="outside"
                      name="username"
                      placeholder="Enter your username"
                      type="text"
                      variant="bordered"
                      value={logInData.username}
                      onChange={handleLogInChange}
                    />
                    <Input
                      isRequired
                      endContent={
                        <button type="button" onClick={toggleVisibility}>
                          {isVisible ? (
                            <Icon
                              className="pointer-events-none text-2xl text-default-400"
                              icon="solar:eye-closed-linear"
                            />
                          ) : (
                            <Icon
                              className="pointer-events-none text-2xl text-default-400"
                              icon="solar:eye-bold"
                            />
                          )}
                        </button>
                      }
                      label="Password"
                      labelPlacement="outside"
                      name="password"
                      placeholder="Enter your password"
                      type={isVisible ? "text" : "password"}
                      variant="bordered"
                      value={logInData.password}
                      onChange={handleLogInChange}
                    />
                    <div className="flex w-full items-center justify-between px-1 py-2">
                      <Checkbox defaultSelected name="remember" size="sm">
                        Remember me
                      </Checkbox>
                      <Link className="text-default-500" href="#" size="sm">
                        Forgot password?
                      </Link>
                    </div>
                    <Button className="w-full" color="primary" type="submit">
                      Log In
                    </Button>
                  </Form>
                </div>
              </div>
            </div>
          </ModalBody>
        </ModalContent>
      </Modal>
    </>
  );
}