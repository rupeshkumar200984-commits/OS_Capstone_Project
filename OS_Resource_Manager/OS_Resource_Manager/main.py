from modules.simulation import run_complete_simulation
from modules.cpu_scheduling import run_cpu_menu
from modules.memory_management import run_memory_menu
from modules.deadlock import run_deadlock_menu
from modules.disk_scheduling import run_disk_menu
from modules.analytics import show_latest_reports

def main():
    while True:
        print("\n" + "=" * 54)
        print("             OS RESOURCE MANAGER")
        print("=" * 54)
        print("1. CPU Scheduling")
        print("2. Memory Management")
        print("3. Deadlock Management")
        print("4. Disk Scheduling")
        print("5. View Latest Reports")
        print("6. Run Complete Simulation")
        print("0. Exit")
        choice = input("\nSelect an option: ").strip()

        try:
            if choice == "1":
                run_cpu_menu()
            elif choice == "2":
                run_memory_menu()
            elif choice == "3":
                run_deadlock_menu()
            elif choice == "4":
                run_disk_menu()
            elif choice == "5":
                show_latest_reports()
            elif choice == "6":
                run_complete_simulation()
            elif choice == "0":
                print("Exiting OS Resource Manager. Goodbye!")
                break
            else:
                print("Invalid option. Enter a number from 0 to 6.")
        except (ValueError, IndexError) as exc:
            print(f"Input error: {exc}")
        except Exception as exc:
            print(f"Unexpected error: {exc}")

if __name__ == "__main__":
    main()
