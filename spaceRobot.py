import random
import time


class RobotEspacial:
    def __init__(self, nombre="EXPLORER-1"):
        self.nombre = nombre
        self.posicion = [0, 0]
        self.energia = 100
        self.recursos = 0
        self.log = []

    def mover(self, dx, dy):
        costo = (abs(dx) + abs(dy)) * 5
        if self.energia < costo:
            self._registrar(f"⚠️ Energía insuficiente para moverse ({self.energia}/{costo})")
            return False
        self.posicion[0] += dx
        self.posicion[1] += dy
        self.energia -= costo
        self._registrar(f"🚀 Movido a posición {self.posicion} (energía: {self.energia})")
        return True

    def escanear(self):
        if self.energia < 10:
            self._registrar("⚠️ Energía insuficiente para escanear")
            return None
        self.energia -= 10
        hallazgo = random.choice([
            "planeta rocoso", "campo de asteroides", "nebulosa",
            "nave abandonada", "cristal de energía", "nada de interés"
        ])
        self._registrar(f"🔭 Escaneo en {self.posicion}: {hallazgo}")
        return hallazgo

    def recolectar(self):
        hallazgo = self.escanear()
        if hallazgo in ("cristal de energía", "nave abandonada"):
            ganancia = random.randint(5, 20)
            self.recursos += ganancia
            self._registrar(f"⛏️ Recolectados {ganancia} recursos (total: {self.recursos})")
        else:
            self._registrar("❌ No había nada que recolectar aquí")

    def recargar(self, cantidad=30):
        self.energia = min(100, self.energia + cantidad)
        self._registrar(f"🔋 Energía recargada a {self.energia}")

    def estado(self):
        return (f"\n--- ESTADO DE {self.nombre} ---\n"
                f"Posición: {self.posicion}\n"
                f"Energía: {self.energia}/100\n"
                f"Recursos: {self.recursos}\n")

    def _registrar(self, mensaje):
        self.log.append(mensaje)
        print(mensaje)


def mision_automatica(robot, pasos=8):
    print(f"\n=== INICIANDO MISIÓN DE {robot.nombre} ===\n")
    for _ in range(pasos):
        if robot.energia < 15:
            robot.recargar()
            time.sleep(0.3)
            continue

        accion = random.choice(["mover", "escanear", "recolectar"])
        if accion == "mover":
            dx, dy = random.choice([(1, 0), (-1, 0), (0, 1), (0, -1)])
            robot.mover(dx, dy)
        elif accion == "escanear":
            robot.escanear()
        else:
            robot.recolectar()
        time.sleep(0.3)

    print(robot.estado())


if __name__ == "__main__":
    robot = RobotEspacial("EXPLORER-1")
    mision_automatica(robot, pasos=10)
