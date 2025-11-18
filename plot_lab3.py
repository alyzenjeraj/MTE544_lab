import pandas as pd
import matplotlib.pyplot as plt

def load_csv(path):
    df = pd.read_csv(path)

    # Convert nanoseconds to seconds (stamp is in nanoseconds)
    df["t"] = (df[" stamp"] - df[" stamp"].iloc[0]) / 1e9

    return df


# ------------------------------
# Plot XY Trajectory
# ------------------------------
def plot_xy(df, title, savefile):
    plt.figure(figsize=(8, 6))
    plt.plot(df["odom_x"], df[" odom_y"], label="Odometry", linewidth=2)
    plt.plot(df[" pf_x"], df[" pf_y"], label="Particle Filter", linewidth=2)
    plt.title(title)
    plt.xlabel("X (m)")
    plt.ylabel("Y (m)")
    plt.grid(True)
    plt.legend()
    plt.savefig(savefile, dpi=300)
    print(f"Saved {savefile}")
    plt.close()


# ------------------------------
# Plot Theta vs Time
# ------------------------------
def plot_theta(df, title, savefile):
    plt.figure(figsize=(8, 6))
    plt.plot(df["t"], df[" odom_th"], label="Odometry θ", linewidth=2)
    plt.plot(df["t"], df[" pf_th"], label="PF θ", linewidth=2)
    plt.title(title)
    plt.xlabel("Time (s)")
    plt.ylabel("Theta (rad)")
    plt.grid(True)
    plt.legend()
    plt.savefig(savefile, dpi=300)
    print(f"Saved {savefile}")
    plt.close()


# ------------------------------------------------------
# FILE LIST — rename these to match your actual filenames
# ------------------------------------------------------
files = {
    "Part 5": "robotPose_part5.csv",
    # "Part 6.1 Misaligned": "robotPose_part6_1.csv",
    # "Part 6.2 Noise Low": "robotPose_part6_2_low.csv",
    # "Part 6.2 Noise High": "robotPose_part6_2_high.csv",
}

for label, fname in files.items():
    try:
        df = load_csv(fname)

        plot_xy(df,
                f"{label}: XY Trajectory",
                f"{fname}_xy.png")

        plot_theta(df,
                   f"{label}: Theta vs Time",
                   f"{fname}_theta.png")

    except Exception as e:
        print(f"Error processing {fname}: {e}")
