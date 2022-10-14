
import argparse
from src.selector import DeviceSelector
from src.front import AppFront


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--device', type=str, default='Mic',
                        help='device type (Mic, Mock), Mic default')
    args = parser.parse_args()

    DeviceSelector(device=args.device)
    AppFront.run()
