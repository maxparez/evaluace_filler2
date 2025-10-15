#!/usr/bin/env python3
"""
LimeSurvey Form Filler - CLI Entry Point

Automated form completion for educational evaluation surveys
"""

import sys
import argparse
from pathlib import Path

from src.form_filler import FormFiller
from src.config_loader import ConfigValidationError


def main():
    """Main CLI entry point"""

    parser = argparse.ArgumentParser(
        description='LimeSurvey Form Filler - Automated form completion',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Run with default settings (headless)
  python main.py data/Bruntal_Pionyrska_MS_360_consolidated.json

  # Run with visible browser (headed mode)
  python main.py data/config.json --headed

  # Override access code
  python main.py data/config.json --code ABC123

  # Verbose logging
  python main.py data/config.json --verbose

  # All options combined
  python main.py data/config.json --headed --code XYZ789 --verbose
        """
    )

    parser.add_argument(
        'config',
        help='Path to JSON configuration file'
    )

    parser.add_argument(
        '--headed',
        action='store_true',
        help='Run browser in headed (visible) mode for debugging'
    )

    parser.add_argument(
        '--code',
        type=str,
        help='Override access code from JSON'
    )

    parser.add_argument(
        '--verbose', '-v',
        action='store_true',
        help='Enable verbose/debug logging'
    )

    args = parser.parse_args()

    # Validate config file exists
    config_path = Path(args.config)
    if not config_path.exists():
        print(f"❌ Error: Configuration file not found: {args.config}")
        sys.exit(1)

    try:
        # Create form filler
        filler = FormFiller(
            config_path=str(config_path),
            headless=not args.headed,
            verbose=args.verbose,
            code_override=args.code
        )

        # Run form filling
        success = filler.run()

        # Exit with appropriate code
        if success:
            print("\n✅ Form filling completed successfully!")
            sys.exit(0)
        else:
            print("\n❌ Form filling failed!")
            sys.exit(1)

    except ConfigValidationError as e:
        print(f"\n❌ Configuration validation error: {e}")
        sys.exit(1)

    except KeyboardInterrupt:
        print("\n\n⚠️  Interrupted by user")
        sys.exit(130)

    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        if args.verbose:
            import traceback
            traceback.print_exc()
        sys.exit(1)


if __name__ == '__main__':
    main()
