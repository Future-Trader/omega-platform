from __future__ import annotations

import argparse

from scripts.core.configuration import config
from scripts.core.engine import GeneratorEngine
from scripts.core.registry import register_builtin_generators, registry


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="OMEGA Platform Code Generator"
    )

    parser.add_argument(
        "generator",
        nargs="?",
        help="Generator to execute.",
    )

    parser.add_argument(
        "--list",
        action="store_true",
        help="List available generators.",
    )

    parser.add_argument(
        "--all",
        action="store_true",
        help="Run all registered generators.",
    )

    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Show what would be generated without writing files.",
    )

    parser.add_argument(
        "--overwrite",
        action="store_true",
        help="Overwrite existing generated files.",
    )

    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()

    if args.dry_run:
        config.dry_run = True

    if args.overwrite:
        config.overwrite = True

    register_builtin_generators()

    engine = GeneratorEngine(
        config=config,
        registry=registry,
    )

    print("=" * 60)
    print(f"{config.project_name} Code Generator")
    print(f"Version : {config.version}")
    print("=" * 60)

    if args.list:
        print()
        print("Available generators:")
        print()

        for item in engine.list_generators():
            print(
                f"  {item['name']:<15} "
                f"{item['description']}"
            )

        return 0

    if args.all:
        results = engine.run_all()

    elif args.generator:
        results = [
            engine.run(args.generator)
        ]

    else:
        parser.print_help()
        return 0

    print()

    failed = False

    for result in results:
        print(
            f"[{'OK' if result.success else 'FAILED'}] "
            f"{result.generator}"
        )

        for path in result.files_created:
            print(f"  [CREATE] {path}")

        for path in result.files_modified:
            print(f"  [MODIFY] {path}")

        for path in result.files_skipped:
            print(f"  [SKIP]   {path}")

        for error in result.errors:
            print(f"  [ERROR]  {error}")

        if not result.success:
            failed = True

    print()
    print("=" * 60)

    if failed:
        print("Generation completed with errors.")
        return 1

    print("Generation completed successfully.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
