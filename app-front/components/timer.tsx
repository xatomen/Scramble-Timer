"use client"

import React, { useState, useEffect, useRef } from 'react';
import {Card, CardHeader, CardBody, CardFooter} from "@heroui/card";

export default function Timer() {
    // Estado para almacenar el tiempo transcurrido en milisegundos
    const [time, setTime] = useState(0);
    // Estado para controlar si el cronómetro está en ejecución o no
    const [running, setRunning] = useState(false);
    // Estado para almacenar los tiempos guardados
    const [savedTimes, setSavedTimes] = useState<number[]>([]);
    // Referencia para almacenar el identificador del intervalo
    const intervalRef = useRef<NodeJS.Timeout | null>(null);

    // useEffect para manejar los eventos de teclado
    useEffect(() => {
        // Función para manejar el cronómetro al presionar la tecla
        const handleKeyDown = (event: KeyboardEvent) => {
            if (event.code === 'Space') {
                // Detener el cronómetro si está en ejecución
                if (running) {
                    setRunning(false);
                    // Guardar el tiempo actual en el estado de los tiempos
                    setSavedTimes((prevTimes) => [...prevTimes, time]);
                }
                // Reiniciar el cronómetro si no está en ejecución y el tiempo es diferente de cero
                if(!running && time !== 0) {
                    setTime(0);
                }
            }
        };

        // Función para manejar el cronómetro al soltar la tecla
        const handleKeyUp = (event: KeyboardEvent) => {
            // Iniciar el cronómetro si no está en ejecución y el tiempo es diferente de cero
            if (event.code === 'Space' && !running && time !== 0) {
                setRunning(false);
            }
            // Reiniciar el cronómetro si no está en ejecución y el tiempo es igual a cero
            else if (event.code === 'Space' && time === 0) {
                setTime(0);
                setRunning(true);
            }
        };

        // Agregar los event listeners para los eventos de teclado
        window.addEventListener('keydown', handleKeyDown);
        window.addEventListener('keyup', handleKeyUp);

        return () => {
            window.removeEventListener('keydown', handleKeyDown);
            window.removeEventListener('keyup', handleKeyUp);
        };

    }, [running, time]);

    // useEffect para manejar el intervalo del cronómetro
    useEffect(() => {
        if (running) {
            // Calcular el tiempo de inicio restando el tiempo transcurrido
            const startTime = Date.now() - time;
            // Establecer un intervalo que actualiza el tiempo cada 10 milisegundos
            intervalRef.current = setInterval(() => {
                setTime(Date.now() - startTime);
            }, 10);
        } else if (intervalRef.current) {
            // Limpiar el intervalo si el cronómetro se detiene
            clearInterval(intervalRef.current);
            intervalRef.current = null;
        }

        // Limpiar el intervalo cuando el componente se desmonte
        return () => {
            if (intervalRef.current) {
                clearInterval(intervalRef.current);
            }
        };
    }, [running]);

    // Función para formatear el tiempo en segundos y milisegundos
    const formatTime = (time: number) => {
        const seconds = Math.floor(time / 1000);
        const milliseconds = time % 1000;
        return `${seconds}.${milliseconds.toString().padStart(3, '0')}`;
    };

    return (
        <div className="flex justify-center items-center h-full w-full">
            <div className="timer text-9xl">
                {formatTime(time)}
            </div>
            <div className="md:absolute md:right-0 m-4">
                <Card>
                    <CardHeader className="justify-center">
                        <h2 className="text-lg">Times</h2>
                    </CardHeader>
                    <CardBody>
                        <ul className="divide-y divide-gray-200">
                            {
                                savedTimes.map((num, index) => (
                                    <li key={index} className="py-2">
                                        <span>{formatTime(num)}</span>
                                    </li>
                                ))
                            }
                        </ul>
                    </CardBody>
                </Card>
            </div>
        </div>
    );
}