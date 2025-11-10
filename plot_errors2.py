import os
import math
import argparse
import matplotlib.pyplot as plt
from utilities import FileReader


def load_csv(path):
    """Load CSV using the lab's FileReader and return (headers, rows, time_s)."""
    headers, rows = FileReader(path).read_file()
    t0 = rows[0][-1]
    time_s = [(r[-1] - t0) / 1e9 for r in rows]  # ns -> s
    return headers, rows, time_s


# ---------------------------------------------------------
#  PLOTTING HELPERS
# ---------------------------------------------------------
def plot_point_errors(linear_csv, angular_csv, title_prefix="Point"):
    """
    Make the {e-t, eDot-t} plot for BOTH linear and angular for a point experiment.
    """
    lin_h, lin_rows, t_lin = load_csv(linear_csv)
    ang_h, ang_rows, t_ang = load_csv(angular_csv)

    fig, axes = plt.subplots(1, 2, figsize=(14, 6))
    fig.suptitle(f"{title_prefix} – error vs time", fontsize=14)

    # ---- LEFT: linear errors ----
    axes[0].plot(t_lin, [r[0] for r in lin_rows], label="e_lin")
    if len(lin_h) > 1:
        axes[0].plot(t_lin, [r[1] for r in lin_rows], label="edot_lin")
    if len(lin_h) > 2:
        axes[0].plot(t_lin, [r[2] for r in lin_rows], label="eint_lin")
    axes[0].set_title("Linear errors")
    axes[0].set_xlabel("Time [s]")
    axes[0].set_ylabel("Error")
    axes[0].grid(True)
    axes[0].legend()

    # ---- RIGHT: angular errors ----
    axes[1].plot(t_ang, [r[0] for r in ang_rows], label="e_ang")
    if len(ang_h) > 1:
        axes[1].plot(t_ang, [r[1] for r in ang_rows], label="edot_ang")
    if len(ang_h) > 2:
        axes[1].plot(t_ang, [r[2] for r in ang_rows], label="eint_ang")
    axes[1].set_title("Angular errors")
    axes[1].set_xlabel("Time [s]")
    axes[1].set_ylabel("Error")
    axes[1].grid(True)
    axes[1].legend()

    plt.tight_layout()
    plt.show()


def plot_point_pose(robot_pose_csv, title_prefix="Point"):
    """
    Make {x-t, y-t, th-t} from robot_pose.csv
    """
    pose_h, pose_rows, t = load_csv(robot_pose_csv)

    plt.figure(figsize=(10, 5))
    plt.plot(t, [r[0] for r in pose_rows], label="x(t)")
    plt.plot(t, [r[1] for r in pose_rows], label="y(t)")
    plt.plot(t, [r[2] for r in pose_rows], label="theta(t)")
    plt.title(f"{title_prefix} – pose vs time")
    plt.xlabel("Time [s]")
    plt.ylabel("Value")
    plt.grid(True)
    plt.legend()
    plt.tight_layout()
    plt.show()


def plot_point_xy(robot_pose_csv, title_prefix="Point"):
    """
    Make {x-y} from robot_pose.csv
    """
    _, pose_rows, _ = load_csv(robot_pose_csv)

    plt.figure(figsize=(6, 6))
    plt.plot([r[0] for r in pose_rows], [r[1] for r in pose_rows], label=title_prefix)
    plt.title(f"{title_prefix} – x–y path")
    plt.xlabel("x [m]")
    plt.ylabel("y [m]")
    plt.axis("equal")
    plt.grid(True)
    plt.legend()
    plt.tight_layout()
    plt.show()


def plot_point_phase(linear_csv, angular_csv, title_prefix="Point"):
    """
    Make {e–edot} for linear and angular on same figure.
    """
    lin_h, lin_rows, _ = load_csv(linear_csv)
    ang_h, ang_rows, _ = load_csv(angular_csv)

    plt.figure(figsize=(6, 6))
    if len(lin_h) >= 2:
        plt.plot([r[0] for r in lin_rows], [r[1] for r in lin_rows],
                 label="linear e–e_dot")
    if len(ang_h) >= 2:
        plt.plot([r[0] for r in ang_rows], [r[1] for r in ang_rows],
                 label="angular e–e_dot")
    plt.title(f"{title_prefix} – e vs e_dot")
    plt.xlabel("e")
    plt.ylabel("e_dot")
    plt.grid(True)
    plt.legend()
    plt.tight_layout()
    plt.show()


def plot_traj_xy(robot_pose_csv, label="trajectory"):
    """
    For part 6: plot only x–y for parabola/sigmoid
    """
    _, pose_rows, _ = load_csv(robot_pose_csv)
    plt.plot([r[0] for r in pose_rows], [r[1] for r in pose_rows], label=label)


def plot_traj_errors(linear_csv, angular_csv, title_prefix="Trajectory"):
    """
    Optional: show e, e_dot during trajectory
    """
    lin_h, lin_rows, t_lin = load_csv(linear_csv)
    ang_h, ang_rows, t_ang = load_csv(angular_csv)

    fig, ax = plt.subplots(1, 2, figsize=(14, 5))
    fig.suptitle(f"{title_prefix} – errors vs time", fontsize=14)

    # linear
    ax[0].plot(t_lin, [r[0] for r in lin_rows], label="e_lin")
    if len(lin_h) > 1:
        ax[0].plot(t_lin, [r[1] for r in lin_rows], label="edot_lin")
    ax[0].set_title("Linear")
    ax[0].set_xlabel("Time [s]")
    ax[0].grid(True)
    ax[0].legend()

    # angular
    ax[1].plot(t_ang, [r[0] for r in ang_rows], label="e_ang")
    if len(ang_h) > 1:
        ax[1].plot(t_ang, [r[1] for r in ang_rows], label="edot_ang")
    ax[1].set_title("Angular")
    ax[1].set_xlabel("Time [s]")
    ax[1].grid(True)
    ax[1].legend()

    plt.tight_layout()
    plt.show()


# ---------------------------------------------------------
#  MAIN
# ---------------------------------------------------------
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Lab MTE 544 plotting helper")
    parser.add_argument("--point_p", type=str, help="folder with linear.csv, angular.csv, robot_pose.csv for POINT P run")
    parser.add_argument("--point_pid", type=str, help="folder with linear.csv, angular.csv, robot_pose.csv for POINT PID run")
    parser.add_argument("--parabola", type=str, help="folder with linear.csv, angular.csv, robot_pose.csv for PARABOLA PID run")
    parser.add_argument("--sigmoid", type=str, help="folder with linear.csv, angular.csv, robot_pose.csv for SIGMOID PID run")
    args = parser.parse_args()

    # 1) POINT – P
    if args.point_p:
        lin = os.path.join(args.point_p, "linear.csv")
        ang = os.path.join(args.point_p, "angular.csv")
        pose = os.path.join(args.point_p, "robot_pose.csv")
        print("[*] Plotting POINT – P controller")
        plot_point_errors(lin, ang, title_prefix="Point – P")
        plot_point_pose(pose, title_prefix="Point – P")
        plot_point_xy(pose, title_prefix="Point – P")
        plot_point_phase(lin, ang, title_prefix="Point – P")

    # 2) POINT – PID
    if args.point_pid:
        lin = os.path.join(args.point_pid, "linear.csv")
        ang = os.path.join(args.point_pid, "angular.csv")
        pose = os.path.join(args.point_pid, "robot_pose.csv")
        print("[*] Plotting POINT – PID controller")
        plot_point_errors(lin, ang, title_prefix="Point – PID")
        plot_point_pose(pose, title_prefix="Point – PID")
        plot_point_xy(pose, title_prefix="Point – PID")
        plot_point_phase(lin, ang, title_prefix="Point – PID")

    # 3) TRAJECTORY – PARABOLA (x–y only is required)
    if args.parabola:
        pose_par = os.path.join(args.parabola, "robot_pose.csv")
        print("[*] Plotting PARABOLA trajectory")
        plt.figure(figsize=(6, 6))
        plot_traj_xy(pose_par, label="parabola")
        plt.title("Trajectory tracking – parabola")
        plt.xlabel("x [m]")
        plt.ylabel("y [m]")
        plt.axis("equal")
        plt.grid(True)
        plt.legend()
        plt.tight_layout()
        plt.show()

        # optional errors
        lin_par = os.path.join(args.parabola, "linear.csv")
        ang_par = os.path.join(args.parabola, "angular.csv")
        if os.path.exists(lin_par) and os.path.exists(ang_par):
            plot_traj_errors(lin_par, ang_par, title_prefix="Parabola")

    # 4) TRAJECTORY – SIGMOID
    if args.sigmoid:
        pose_sig = os.path.join(args.sigmoid, "robot_pose.csv")
        print("[*] Plotting SIGMOID trajectory")
        plt.figure(figsize=(6, 6))
        plot_traj_xy(pose_sig, label="sigmoid")
        plt.title("Trajectory tracking – sigmoid")
        plt.xlabel("x [m]")
        plt.ylabel("y [m]")
        plt.axis("equal")
        plt.grid(True)
        plt.legend()
        plt.tight_layout()
        plt.show()

        # optional errors
        lin_sig = os.path.join(args.sigmoid, "linear.csv")
        ang_sig = os.path.join(args.sigmoid, "angular.csv")
        if os.path.exists(lin_sig) and os.path.exists(ang_sig):
            plot_traj_errors(lin_sig, ang_sig, title_prefix="Sigmoid")
