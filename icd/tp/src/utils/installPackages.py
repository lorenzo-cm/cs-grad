import subprocess

def install_packages(requirements_file):
    with open(requirements_file, 'r') as file:
        packages = [line.strip() for line in file]

    for package in packages:
        try:
            subprocess.check_call(['pip', 'install', package])
            print(f'Successfully installed {package}')
        except subprocess.CalledProcessError:
            print(f'Failed to install {package}')

# Example usage
requirements_file = 'requirements.txt'
install_packages(requirements_file)