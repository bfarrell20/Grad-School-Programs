import matplotlib.pyplot as plt

# Updated data from the second run
elapsed = list(range(1, 61))
estimated_users = [
    87, 169, 244, 320, 388, 451, 514, 579, 637, 687,
    739, 796, 848, 896, 934, 977, 1016, 1054, 1096, 1131,
    1177, 1212, 1239, 1257, 1293, 1320, 1352, 1379, 1398, 1429,
    1454, 1470, 1494, 1514, 1534, 1551, 1564, 1589, 1608, 1627,
    1637, 1654, 1666, 1678, 1688, 1704, 1715, 1721, 1732, 1748,
    1759, 1771, 1778, 1787, 1794, 1802, 1806, 1809, 1815, 1820
]

# Plotting the estimated unique users over time
plt.figure(figsize=(10, 6))
plt.plot(elapsed, estimated_users, marker='o', color='blue', linestyle='-')
plt.title('Estimated Unique Users Over Time')
plt.xlabel('Elapsed Time (seconds)')
plt.ylabel('Estimated Unique Users')
plt.grid(True)
plt.tight_layout()

plt.show()
