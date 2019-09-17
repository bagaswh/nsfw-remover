def init_draw():
    x = np.linspace(0, 2 * np.pi, 120)
    y = np.linspace(0, 2 * np.pi, 100).reshape(-1, 1)
    image = np.sin(x) + np.cos(y)

    global ax1, im1, t1, t2
    ax1 = plt.subplot(1, 2, 1)
    im1 = ax1.imshow(image)
    plt.ion()
    t1 = ax1.text(0, 125, "N/A")
    t2 = ax1.text(0, -10, "N/A")


def draw(title1, title2, image, frame_num):
    global ax1, im1, t1, t2
    plt.title(title1)
    t1.set_text(title2)
    t2.set_text(frame_num)
    im1.set_data(image)
    plt.savefig(f"./examples/frame-{frame_num}.png")
    plt.pause(0.05)