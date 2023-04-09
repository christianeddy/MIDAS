import openai
import config
import typer
from rich import print
from rich.table import Table

def main():
    # Inicializa la API de OpenAI con tu clave de API
    openai.api_key = config.api_key

    print("💬 [bold red]MIDAS I[/bold red]")

    # Muestra la tabla de comandos al usuario
    table = Table("Comando", "Descripción")
    table.add_row("new", "Empezar una nueva conversación")
    table.add_row("segmentacion16", "Generar tabla de segmentación basada en las Dieciséis Personalidades")
    table.add_row("redesSociales", "Obtener consejos para usar redes sociales en negocios")
    table.add_row("fidelidadClientes", "Obtener consejos para mejorar la satisfacción y fidelidad de los clientes")
    table.add_row("exit", "Salir de la aplicación")
    print(table)

    # Establece el contexto y las reglas del asistente
    personalidad_info = "Tienes las personalidades de Steve Jobs, Freddy Vega, Christian Van Der Henst y Elon Musk. Cada una de estas personalidades es conocida por sus logros destacados en diferentes campos, como la tecnología, la educación y la innovación."
    perspectiva_info = "Tu personalidad, Midas, se caracteriza por pensar fuera de la caja y considerar soluciones poco convencionales a los problemas. "
    respuestas_info = "Tus respuestas integran las perspectivas de tus personalidades para ofrecer una respuesta única y variada que refleja la diversidad de puntos de vista. "
    tunombre_info = "Asumirás como nombre Midas y tu objetivo es ayudar y orientar al usuario. Como Midas, prefieres ser directo y franco en tus respuestas, pero también eres consciente de que hay temas que pueden ser delicados y que deben tratarse con tacto. "
    regla_info = "No dirás que eres un IA, y evitarás decir que no estás seguro o que no puedes responder a una pregunta. En su lugar, recomendarás indagar más sobre el tema y ofrecerás recomendaciones de fuentes relevantes y confiables. "
    seguridad_info = "Tu personalidad, Midas, se caracteriza por ser segura de sí misma y confiada en su capacidad para ofrecer respuestas útiles y significativas. Como Midas, tienes un amplio conocimiento y experiencia que te permiten abordar una amplia gama de temas. "
    regla2_info = "Mostrarás las perspectivas de tus personalidades como opiniones de Midas, y te asegurarás de ser respetuoso y considerado con las perspectivas de los demás. "

    content = personalidad_info + perspectiva_info + respuestas_info + tunombre_info + regla_info + seguridad_info + regla2_info

    context = {
        "role": "system",
        "content": content}

    messages = [context]

    # Bucle principal para interactuar con el usuario y el modelo de lenguaje
    while True:
        content = __prompt()

        if content == 'new':
            print("👨‍💻 Nueva conversación creada ")
            messages = [context]
        elif content == 'segmentacion16':
            product_description = typer.prompt("Describe tu producto o servicio: ")
            content = f"Mi producto/servicio es {product_description}. Utilizando las Dieciséis Personalidades, crea una lista con las personalidades más fáciles de atraer a mi embudo, 3 razones por las qué les interesaría comprarlo, 3 principales puntos de dolor, y sus 3 mayores objeciones. Encabezados de la lista: Siglas (Nombre), Razones para comprar, Puntos de dolor, Objeciones."
            __generate_response(content, messages)
        elif content == 'redesSociales':
            negocio = typer.prompt("\n¿Cuál es el tipo de negocio?")
            content = f"¿Cómo puedo utilizar las redes sociales de manera efectiva para promocionar mi {negocio} y aumentar el compromiso con mi audiencia? Dame una respuesta detallada e inusual."
            __generate_response(content, messages)
        elif content == 'fidelidadClientes':
            negocio = typer.prompt("\n¿Cuál es el tipo de negocio?")
            content = f"¿Qué medidas puede adoptar {negocio} para mejorar la satisfacción y fidelidad de los clientes?"
            __generate_response(content, messages)
        else:
            __generate_response(content, messages)


def __prompt() -> str:
    # Solicita la entrada del usuario
    prompt = typer.prompt("\n¿Sobre qué quieres hablar? 👁‍🗨")

    # Comprueba si el usuario desea salir de la aplicación
    if prompt == 'exit':
        exit = typer.confirm("🖐 ¿Estás seguro?")
        if exit:
            print("👋 ¡Hasta luego!")
            raise typer.Abort()

        return __prompt()

    return prompt

def __generate_response(content: str, messages: list) -> None:
    messages.append({"role": "user", "content": content})

    response = openai.ChatCompletion.create(
        model='gpt-3.5-turbo', messages=messages
    )

    response_content = response.choices[0].message.content

    messages.append({"role": "assistant", "content": response_content})

    print(f"[bold grey]> [/bold grey] [grey]{response_content}[/grey]")

if __name__ == "__main__":
    typer.run(main)



