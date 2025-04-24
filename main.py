import argparse
import cv2
import time
from pathlib import Path
from ultralytics import YOLO


def parse_arguments():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(description="YOLOv11 webcam detection with OpenVINO")
    parser.add_argument(
        "--model", 
        type=str, 
        default="yolo11s.pt", 
        help="Model path or name"
    )
    parser.add_argument(
        "--device", 
        type=str, 
        default="intel:cpu",
        help="OpenVINO device: 'intel:cpu', 'intel:gpu', or 'intel:npu'"
    )
    parser.add_argument(
        "--conf", 
        type=float, 
        default=0.25, 
        help="Confidence threshold"
    )
    parser.add_argument(
        "--cam-id", 
        type=int, 
        default=0, 
        help="Webcam device ID"
    )
    parser.add_argument(
        "--export-only", 
        action="store_true", 
        help="Only export the model, don't run inference"
    )
    return parser.parse_args()


def export_model(model_path):
    """Export PyTorch model to OpenVINO format."""
    print(f"Loading YOLOv11 model from {model_path}...")
    model = YOLO(model_path)
    
    # Extract model name without extension
    model_name = Path(model_path).stem
    export_path = f"{model_name}_openvino_model"
    
    print(f"Exporting model to OpenVINO format at {export_path}/...")
    model.export(format="openvino")
    
    return export_path


def main():
    """Main function."""
    args = parse_arguments()
    
    # Export model to OpenVINO format if needed
    if Path(args.model).suffix == ".pt":
        export_path = export_model(args.model)
    else:
        # Assume it's already an OpenVINO model directory
        export_path = args.model
    
    if args.export_only:
        print(f"Model exported to {export_path}")
        return
    
    # Load OpenVINO model
    print(f"Loading OpenVINO model from {export_path}...")
    ov_model = YOLO(export_path)
    
    # Initialize webcam
    print(f"Opening webcam (ID: {args.cam_id})...")
    cap = cv2.VideoCapture(args.cam_id)
    if not cap.isOpened():
        print(f"Error: Could not open webcam with ID {args.cam_id}")
        return
    
    # Get webcam properties
    frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    
    print(f"Webcam resolution: {frame_width}x{frame_height}")
    print(f"Press 'q' to quit")
    
    # Main processing loop
    while True:
        ret, frame = cap.read()
        if not ret:
            print("Error: Failed to capture frame from webcam")
            break
        
        # Perform inference with specified device and track performance
        start_time = time.time()
        results = ov_model(frame, conf=args.conf, device=args.device)
        inference_time = time.time() - start_time
        fps = 1 / inference_time
        
        # Use the built-in visualization method
        annotated_frame = results[0].plot()
        
        # Add performance metrics overlay
        cv2.putText(
            annotated_frame, 
            f"Inference: {inference_time*1000:.1f}ms ({fps:.1f} FPS)", 
            (10, 30), 
            cv2.FONT_HERSHEY_SIMPLEX, 
            0.7, 
            (0, 255, 0), 
            2
        )
        
        # Display the frame
        cv2.imshow("YOLOv11 OpenVINO Detection", annotated_frame)
        
        # Check for exit key
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    
    # Clean up
    cap.release()
    cv2.destroyAllWindows()
    print("Webcam detection stopped")


if __name__ == "__main__":
    main()