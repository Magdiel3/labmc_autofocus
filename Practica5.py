from autofocus_system import autofocus_PI
import matplotlib.pyplot as plt

t_step = 0.0
t1 = 0.05
step = 1
dt = 0.0001
title = ""

def conf_plot(title = "Time Response"):
    title = title
    print(f"Configuring autofocus system for {title} plots")
    _system = autofocus_PI(250,55)
    t, u = _system.get_step_input(t_step,t1,step,dt)
    t = _system.time_to_ms(t)
    plt.figure()
    plt.title(title)
    plt.plot(t, u, "b--", label="u(s)")
    plt.xlabel("time [ms]")
    plt.ylabel("lens displacement [mm]")

def plot_response(kp, ki, color = "blue", label = "z(t)"):
    system = autofocus_PI(kp, ki)
    system.print_tf()
    (t, y) = system.step_response(t_step,t1,step,dt)

    plt.plot(t, y, color, label=label)

# Print student data
print("Magdiel Martínez")
print("1660362\n")

# Configure plot
conf_plot("Time Response (ki = 55)")

# Generate responses
fixed_ki = [(100, "black"), (250, "brown"), (500, "red"), (750, "green"), (900, "y")]

for kp, color in fixed_ki:
    plot_response(kp,55,color,f"z(t), kp={kp}")

# Display plot
plt.legend()
plt.savefig("fixed_ki.png")
plt.show()

# Configure plot
conf_plot("Time Response (kp = 500)")

# Generate responses
fixed_kp = [(20, "black"), (35, "brown"), (55, "red"), (75, "green"), (90, "yellow")]

for ki, color in fixed_kp:
    plot_response(500,ki,color,f"z(t), ki={ki}")

# Display plot
plt.legend()
plt.savefig("fixed_kp.png")
plt.show()

# Explosion
t1 = 0.5
# Configure plot
conf_plot("Time Response (kp = 500, ki = 750)")
plot_response(500,750,"r",f"z(t), kp=500 ki=750")
# Display plot
plt.legend()
plt.savefig("chaos.png")
plt.show()
