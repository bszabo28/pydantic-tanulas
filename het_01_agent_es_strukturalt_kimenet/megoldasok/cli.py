"""6. feladat: parancssori üzenetosztályozó hibakezeléssel."""

import argparse
import sys

from pydantic_ai import models
from pydantic_ai.exceptions import (
    AgentRunError,
    ModelAPIError,
    ModelHTTPError,
    UnexpectedModelBehavior,
    UserError,
)

from .agent import create_agent, demo_model, resolve_model
from .futas_vizsgalata import inspect_run, run_analysis


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Ügyfélüzenet → TicketAnalysis JSON.")
    parser.add_argument("message", help="Az ügyfél üzenete.")
    parser.add_argument("--model", help="Modellazonosító; egyébként PYDANTIC_AI_MODEL.")
    parser.add_argument("--offline", action="store_true", help="Előre megadott tesztválasz.")
    parser.add_argument("--inspect", action="store_true", help="Üzenetsor és használat stderrre.")
    parser.add_argument("--async", dest="asynchronous", action="store_true")
    parser.add_argument(
        "--simulate-invalid-output",
        action="store_true",
        help="Offline hibaút: ismételten érvénytelen kategória.",
    )
    args = parser.parse_args(argv)
    if not args.message.strip():
        parser.error("Az üzenet nem lehet üres.")
    if args.offline and args.model is not None:
        parser.error("Válassz egy futtatási módot: --offline vagy --model.")
    if args.simulate_invalid_output and not args.offline:
        parser.error("A --simulate-invalid-output kapcsolóhoz --offline szükséges.")

    try:
        if args.offline:
            models.ALLOW_MODEL_REQUESTS = False
            model = demo_model(invalid_output=args.simulate_invalid_output)
            print(
                "OFFLINE: előre megadott választ játszunk le; az üzenet értelmezése nem történik meg.",
                file=sys.stderr,
            )
        else:
            model = resolve_model(args.model)
        agent = create_agent(model)
    except (ValueError, UserError) as error:
        print(f"Konfigurációs hiba: {error}", file=sys.stderr)
        return 2

    try:
        result = run_analysis(agent, args.message, asynchronous=args.asynchronous)
    except ModelHTTPError as error:
        print(f"Szolgáltatói HTTP-hiba: {error.status_code}.", file=sys.stderr)
        return 1
    except ModelAPIError:
        print("A modellszolgáltató hívása sikertelen.", file=sys.stderr)
        return 1
    except UnexpectedModelBehavior:
        print("A modell nem adott elfogadható kimenetet a javítási kereten belül.", file=sys.stderr)
        return 1
    except AgentRunError as error:
        print(f"Sikertelen agentfutás: {type(error).__name__}.", file=sys.stderr)
        return 1
    except UserError as error:
        print(f"Használati hiba: {error}", file=sys.stderr)
        return 2
    except TimeoutError:
        print("A futás időtúllépéssel zárult.", file=sys.stderr)
        return 1

    print(result.output.model_dump_json(indent=2))
    if args.inspect:
        inspect_run(result)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
