package main

import (
	"fmt"
	"runtime"
)

func main() {
	fmt.Println("¡Hola desde Go en un contenedor de Docker!")
	fmt.Printf("Estás usando Go versión: %s\n", runtime.Version())
}
