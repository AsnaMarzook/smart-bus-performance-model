import os
import pandas as pd
import matplotlib.pyplot as plt


def ensure_output_dir(path: str) -> None:
    os.makedirs(path, exist_ok=True)


def save_show(fig, out_path: str, show: bool = True) -> None:
    fig.tight_layout()
    fig.savefig(out_path, dpi=300)
    if show:
        plt.show()
    plt.close(fig)


def main():
    # ====== CONFIG ======
    excel_file = "Smart_Bus_Mini_Project_Dataset.xlsx"   # change if your file name differs
    sheet_name = "Mini_Project_Dataset"                  # change if your sheet name differs
    output_dir = "output_graphs"
    show_plots = True  # set False if you only want saved PNG files
    # ====================

    ensure_output_dir(output_dir)

    # Load dataset
    df = pd.read_excel(excel_file, sheet_name=sheet_name)

    # Basic cleaning (optional, safe)
    df["Traffic_Level"] = df["Traffic_Level"].astype(str).str.strip().str.title()
    df["Time_Period"] = df["Time_Period"].astype(str).str.strip().str.title()
    df["Route_ID"] = df["Route_ID"].astype(str).str.strip().str.upper()

    # ---- Graph 1: Waiting Time vs Passenger Arrival Rate (Scatter) ----
    fig1 = plt.figure()
    plt.scatter(df["Passenger_Arrival_Rate (per min)"], df["Average_Waiting_Time (min)"])
    plt.xlabel("Passenger Arrival Rate (passengers/min)")
    plt.ylabel("Average Waiting Time (min)")
    plt.title("Waiting Time vs Passenger Arrival Rate")
    save_show(fig1, os.path.join(output_dir, "01_waiting_time_vs_arrival_rate.png"), show=show_plots)

    # ---- Graph 2: Average Waiting Time by Time Period (Bar) ----
    avg_wait_by_period = df.groupby("Time_Period")["Average_Waiting_Time (min)"].mean()
    # Enforce meaningful order if exists
    period_order = ["Off-Peak", "Normal", "Peak"]
    avg_wait_by_period = avg_wait_by_period.reindex([p for p in period_order if p in avg_wait_by_period.index])

    fig2 = plt.figure()
    avg_wait_by_period.plot(kind="bar")
    plt.xlabel("Time Period")
    plt.ylabel("Average Waiting Time (min)")
    plt.title("Average Waiting Time by Time Period")
    save_show(fig2, os.path.join(output_dir, "02_avg_waiting_time_by_time_period.png"), show=show_plots)

    # ---- Graph 3: Throughput per Route (Bar) ----
    throughput_by_route = df.groupby("Route_ID")["Passengers_Transported (per hour)"].mean().sort_values(ascending=False)

    fig3 = plt.figure()
    throughput_by_route.plot(kind="bar")
    plt.xlabel("Route ID")
    plt.ylabel("Passengers Transported per Hour")
    plt.title("Average Throughput per Route")
    save_show(fig3, os.path.join(output_dir, "03_throughput_per_route.png"), show=show_plots)

    # ---- Graph 4: Occupancy Rate vs Passenger Arrival Rate (Scatter) ----
    fig4 = plt.figure()
    plt.scatter(df["Passenger_Arrival_Rate (per min)"], df["Occupancy_Rate (%)"])
    plt.xlabel("Passenger Arrival Rate (passengers/min)")
    plt.ylabel("Occupancy Rate (%)")
    plt.title("Occupancy Rate vs Passenger Arrival Rate")
    save_show(fig4, os.path.join(output_dir, "04_occupancy_vs_arrival_rate.png"), show=show_plots)

    # ---- Graph 5: Average Delay vs Traffic Level (Line) ----
    delay_by_traffic = df.groupby("Traffic_Level")["Average_Delay (min)"].mean()
    traffic_order = ["Low", "Medium", "High"]
    delay_by_traffic = delay_by_traffic.reindex([t for t in traffic_order if t in delay_by_traffic.index])

    fig5 = plt.figure()
    plt.plot(delay_by_traffic.index, delay_by_traffic.values, marker="o")
    plt.xlabel("Traffic Level")
    plt.ylabel("Average Delay (min)")
    plt.title("Average Delay vs Traffic Level")
    save_show(fig5, os.path.join(output_dir, "05_delay_vs_traffic_level.png"), show=show_plots)

    # ---- Graph 6: Queue Length vs Time Period (Bar) ----
    queue_by_period = df.groupby("Time_Period")["Queue_Length"].mean()
    queue_by_period = queue_by_period.reindex([p for p in period_order if p in queue_by_period.index])

    fig6 = plt.figure()
    queue_by_period.plot(kind="bar")
    plt.xlabel("Time Period")
    plt.ylabel("Average Queue Length")
    plt.title("Average Queue Length by Time Period")
    save_show(fig6, os.path.join(output_dir, "06_queue_length_by_time_period.png"), show=show_plots)

    # ---- Graph 7: Bus Frequency vs Waiting Time (Scatter) ----
    fig7 = plt.figure()
    plt.scatter(df["Bus_Frequency (buses/hour)"], df["Average_Waiting_Time (min)"])
    plt.xlabel("Bus Frequency (buses/hour)")
    plt.ylabel("Average Waiting Time (min)")
    plt.title("Waiting Time vs Bus Frequency")
    save_show(fig7, os.path.join(output_dir, "07_waiting_time_vs_bus_frequency.png"), show=show_plots)

    print(f"\nDone! Saved graphs to: {os.path.abspath(output_dir)}")
    print("Files created:")
    for f in sorted(os.listdir(output_dir)):
        print(" -", f)


if __name__ == "__main__":
    main()

