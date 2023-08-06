import argparse
import sys
from dijkprofile_annotator import annotate

def main():
    '''run annotation'''
    parser = argparse.ArgumentParser(prog='dijkprofile_annotator')
    parser.add_argument('-i', '--input', required=True, help='input surfacelines file')
    parser.add_argument('-o', '--output', required=True, help='output path')
    parser.add_argument('-m', '--model', default='simple', help='model type to use') # also called class_list in the code
    parser.add_argument('-l', '--profile-length', default=512, help='max profile length')
    parser.add_argument('-cm', '--custom-model-path', nargs='?', help="custom model path")
    parser.add_argument('-d', '--device', nargs='?', help="device (either 'cpu' or 'cuda:0'")
    parser.add_argument('-s', '--scaler-path', nargs='?', help='custom scaler path')

    args = parser.parse_args()
    
    annotate(args.input, args.output, class_list=args.model, max_profile_length=args.profile_length, custom_model_path=args.custom_model_path, custom_scaler_path=args.scaler_path, device=args.device)


if __name__ == "__main__":
    sys.exit(main())
