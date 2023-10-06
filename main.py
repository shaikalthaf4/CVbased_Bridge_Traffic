from real_time_stream import RealTimeStream

def main():
    # Initialize real-time stream
    stream = RealTimeStream()
    
    try:
        # Start the real-time stream
        stream.start()
    except KeyboardInterrupt:
        # Handle keyboard interrupt (Ctrl+C) to gracefully exit the application
        print("Real-time stream interrupted. Exiting...")
    finally:
        # Clean up resources (if any) after the stream ends
        print("Cleaning up...")

if __name__ == "__main__":
    # Entry point of the application
    main()
