# run.py
import subprocess
import sys
import os

def check_installations():
    """Check and install required packages"""
    print("🔍 Checking installations...")
    print("-" * 50)
    
    required_packages = [
        ('streamlit', '1.28.1'),
        ('pandas', '2.1.3'),
        ('numpy', '1.24.3'),
        ('plotly', '5.17.0')
    ]
    
    for package, version in required_packages:
        try:
            __import__(package.replace('-', '_'))
            print(f"✅ {package} is already installed")
        except ImportError:
            print(f"📦 Installing {package}...")
            subprocess.check_call([sys.executable, "-m", "pip", "install", f"{package}=={version}"])
    
    print("\n" + "="*60)
    print("🚀 ENTERPRISE RISK INTELLIGENCE PLATFORM")
    print("      Version 3.0 - Professional Edition")
    print("="*60 + "\n")

if __name__ == "__main__":
    check_installations()
    
    # Check if app.py exists
    if not os.path.exists("app.py"):
        print("❌ ERROR: app.py not found!")
        print("Please make sure app.py exists in the current directory.")
        input("Press Enter to exit...")
        sys.exit(1)
    
    print("✅ Starting application...")
    print("🌐 Open your browser and go to: http://localhost:8501")
    print("⏳ Please wait for the application to load...\n")
    
    # Run the Streamlit app
    os.system("streamlit run app.py --server.port 8501 --server.address 0.0.0.0")