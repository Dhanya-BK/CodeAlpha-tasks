"""CodeAlpha Task 4 - Real-time object detection (YOLOv8) + tracking (Deep SORT)."""
import argparse
import time
import zlib

import cv2
from deep_sort_realtime.deepsort_tracker import DeepSort
from ultralytics import YOLO


def color_for(track_id):
    h = zlib.crc32(str(track_id).encode())
    return (h & 255, (h >> 8) & 255, (h >> 16) & 255)


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--source", default="0", help="0 for webcam, or path to a video file")
    p.add_argument("--model", default="yolov8n.pt")
    p.add_argument("--conf", type=float, default=0.4)
    p.add_argument("--save", default="", help="optional output video path, e.g. output.mp4")
    args = p.parse_args()

    model = YOLO(args.model)  # auto-downloads weights on first run
    tracker = DeepSort(max_age=30, n_init=3)
    cap = cv2.VideoCapture(0 if args.source == "0" else args.source)
    if not cap.isOpened():
        raise SystemExit("Could not open video source.")

    writer = None
    if args.save:
        w, h = int(cap.get(3)), int(cap.get(4))
        writer = cv2.VideoWriter(args.save, cv2.VideoWriter_fourcc(*"mp4v"), cap.get(5) or 25, (w, h))

    prev = time.time()
    while True:
        ok, frame = cap.read()
        if not ok:
            break

        result = model(frame, conf=args.conf, verbose=False)[0]
        detections = []
        for box in result.boxes:
            x1, y1, x2, y2 = box.xyxy[0].tolist()
            detections.append(([x1, y1, x2 - x1, y2 - y1], float(box.conf[0]), int(box.cls[0])))

        for t in tracker.update_tracks(detections, frame=frame):
            if not t.is_confirmed():
                continue
            l, tp, r, b = map(int, t.to_ltrb())
            name = model.names[t.det_class] if t.det_class is not None else "object"
            label = f"{name} ID:{t.track_id}"
            c = color_for(t.track_id)
            cv2.rectangle(frame, (l, tp), (r, b), c, 2)
            (tw, th), _ = cv2.getTextSize(label, cv2.FONT_HERSHEY_SIMPLEX, 0.6, 2)
            cv2.rectangle(frame, (l, tp - th - 8), (l + tw + 4, tp), c, -1)
            cv2.putText(frame, label, (l + 2, tp - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)

        now = time.time()
        cv2.putText(frame, f"FPS: {1 / (now - prev + 1e-9):.1f}", (10, 25), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
        prev = now

        if writer:
            writer.write(frame)
        cv2.imshow("Object Detection & Tracking (press q to quit)", frame)
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

    cap.release()
    if writer:
        writer.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
