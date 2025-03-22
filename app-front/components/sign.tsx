"use client";

import { useState } from "react";
import { Button, ButtonGroup } from "@heroui/button";
import {
  Modal,
  ModalContent,
  ModalHeader,
  ModalBody,
  ModalFooter,
  useDisclosure,
} from "@heroui/modal";

export default function Sign() {
  const { isOpen, onOpen, onOpenChange } = useDisclosure();
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");

  const handleSignIn = async () => {
    try {
      const response = await fetch("http://localhost:8000/login", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ email, password }),
      });

      if (!response.ok) {
        throw new Error("Credenciales inválidas");
      }

      const data = await response.json();
      // Guarda el token o maneja la respuesta según sea necesario
      console.log("Inicio de sesión exitoso:", data);
      onOpenChange(); // Cierra el modal
    } catch (err: any) {
      setError(err.message);
    }
  };

  return (
    <>
      <Button onPress={onOpen}>Sign In</Button>
      <Modal isOpen={isOpen} onOpenChange={onOpenChange}>
        <ModalContent>
          <ModalHeader>Sign In</ModalHeader>
          <ModalBody>
            {error && <p style={{ color: "red" }}>{error}</p>}
            <form
              onSubmit={(e) => {
                e.preventDefault();
                handleSignIn();
              }}
            >
              <div>
                <label>Email:</label>
                <input
                  type="email"
                  value={email}
                  onChange={(e) => setEmail(e.target.value)}
                  required
                />
              </div>
              <div>
                <label>Password:</label>
                <input
                  type="password"
                  value={password}
                  onChange={(e) => setPassword(e.target.value)}
                  required
                />
              </div>
            </form>
          </ModalBody>
          <ModalFooter>
            <ButtonGroup>
              <Button onPress={onOpenChange}>Close</Button>
              <Button color="primary" onPress={handleSignIn}>
                Sign In
              </Button>
            </ButtonGroup>
          </ModalFooter>
        </ModalContent>
      </Modal>
    </>
  );
}