from typing import Optional, Tuple

import matplotlib.pyplot as plt
import numpy as np
from mpl_toolkits.mplot3d.art3d import Poly3DCollection


def draw_cube(ax, x0, y0, z0, dx, dy, dz, color, alpha=0.75):
    """Desenha um cubo 3D com faces e bordas."""
    v = np.array(
        [
            [x0, y0, z0],
            [x0 + dx, y0, z0],
            [x0 + dx, y0 + dy, z0],
            [x0, y0 + dy, z0],
            [x0, y0, z0 + dz],
            [x0 + dx, y0, z0 + dz],
            [x0 + dx, y0 + dy, z0 + dz],
            [x0, y0 + dy, z0 + dz],
        ]
    )
    faces = [
        [v[0], v[1], v[2], v[3]],
        [v[4], v[5], v[6], v[7]],
        [v[0], v[1], v[5], v[4]],
        [v[2], v[3], v[7], v[6]],
        [v[1], v[2], v[6], v[5]],
        [v[0], v[3], v[7], v[4]],
    ]
    ax.add_collection3d(
        Poly3DCollection(
            faces, facecolors=[color], edgecolors="black", linewidths=0.3, alpha=alpha
        )
    )


def plot_3d_spatiotemporal(
    coords_spatiotemporal: np.ndarray,
    optimal_scale: Optional[Tuple[float, float]] = None,
    gap: float = 0.02,
    cube_alpha: float = 0.75,
    figsize: Tuple[int, int] = (10, 8),
    elev: float = 25,
    azim: float = 40,
    cmap=None,
    normalize_to_origin: bool = True,
    max_cubes_per_dim: int = 20,
):
    """
    Plota uma visualização 3D espaço-temporal dos dados com cubos coloridos por densidade.

    Args:
        coords_spatiotemporal: Array numpy com shape (N, 3) onde cada linha é [x, y, t]
        optimal_scale: Tupla opcional (spatial_scale, temporal_scale) para definir tamanho dos cubos
        gap: Espaçamento relativo entre cubos (0-1)
        cube_alpha: Transparência dos cubos (0-1)
        figsize: Tamanho da figura (width, height)
        elev: Elevação da câmera 3D
        azim: Azimute da câmera 3D
        cmap: Colormap do matplotlib (padrão: Reds)
        normalize_to_origin: Se True, normaliza coordenadas para começar em 0
        max_cubes_per_dim: Número máximo de cubos por dimensão (para evitar grade muito densa)

    Returns:
        fig, ax: Figura e eixos matplotlib
    """
    if cmap is None:
        cmap = plt.cm.Reds

    # Extrair coordenadas
    x = coords_spatiotemporal[:, 0]
    y = coords_spatiotemporal[:, 1]
    z = coords_spatiotemporal[:, 2]

    # Normalizar para começar em 0 se solicitado
    x_min, y_min, z_min = x.min(), y.min(), z.min()
    x_max, y_max, z_max = x.max(), y.max(), z.max()

    if normalize_to_origin:
        x = x - x_min
        y = y - y_min
        z = z - z_min
        # Após normalização, os mínimos são 0
        x_min, y_min, z_min = 0, 0, 0
        x_max, y_max, z_max = x.max(), y.max(), z.max()

    # Calcular ranges
    x_range = x_max - x_min
    y_range = y_max - y_min
    z_range = z_max - z_min

    # Determinar tamanho dos cubos
    if optimal_scale is not None:
        # Usar a escala ótima fornecida - a grid já está definida
        cs_spatial = optimal_scale[0]  # tamanho do cubo no espaço (x e y)
        ct = optimal_scale[1]  # tamanho do cubo no tempo

        # Calcular número de cubos em cada dimensão baseado na escala ótima
        nx = max(1, int(np.ceil(x_range / cs_spatial)))
        ny = max(1, int(np.ceil(y_range / cs_spatial)))
        nz = max(1, int(np.ceil(z_range / ct)))
    else:
        # Calcular automaticamente baseado nos dados
        # Usar aproximadamente max_cubes_per_dim cubos por dimensão
        cs_spatial = max(x_range, y_range) / max_cubes_per_dim
        ct = z_range / max_cubes_per_dim

        # Calcular número de cubos em cada dimensão
        nx = max(1, int(np.ceil(x_range / cs_spatial)))
        ny = max(1, int(np.ceil(y_range / cs_spatial)))
        nz = max(1, int(np.ceil(z_range / ct)))

        # Limitar número de cubos se necessário
        if nx > max_cubes_per_dim:
            nx = max_cubes_per_dim
            cs_spatial = x_range / nx
        if ny > max_cubes_per_dim:
            ny = max_cubes_per_dim
            cs_spatial = y_range / ny
        if nz > max_cubes_per_dim:
            nz = max_cubes_per_dim
            ct = z_range / nz

    # Calcular índices dos cubos para cada ponto
    ix = np.clip((x / cs_spatial).astype(int), 0, nx - 1)
    iy = np.clip((y / cs_spatial).astype(int), 0, ny - 1)
    iz = np.clip((z / ct).astype(int), 0, nz - 1)

    # Contagem de pontos em cada cubo
    counts = np.zeros((nx, ny, nz), dtype=int)
    for i in range(len(coords_spatiotemporal)):
        counts[ix[i], iy[i], iz[i]] += 1

    max_count = counts.max() if counts.max() > 0 else 1

    # Calcular gap absoluto
    gap_x = cs_spatial * gap
    gap_y = cs_spatial * gap
    gap_z = ct * gap

    # Criar figura
    fig = plt.figure(figsize=figsize)
    ax = fig.add_subplot(111, projection="3d")

    # Desenhar todos os cubos coloridos pelo count
    for cx in range(nx):
        for cy in range(ny):
            for cz in range(nz):
                c = counts[cx, cy, cz]
                norm_val = c / max_count if max_count > 0 else 0.0

                if c == 0:
                    cube_color = (1.0, 1.0, 1.0, 1.0)
                    alpha = 0.10
                else:
                    cube_color = cmap(norm_val)
                    alpha = cube_alpha

                x0 = x_min + cx * cs_spatial + gap_x
                y0 = y_min + cy * cs_spatial + gap_y
                z0 = z_min + cz * ct + gap_z

                draw_cube(
                    ax,
                    x0,
                    y0,
                    z0,
                    cs_spatial - gap_x * 2,
                    cs_spatial - gap_y * 2,
                    ct - gap_z * 2,
                    color=cube_color,
                    alpha=alpha,
                )

    # Configurar eixos
    ax.set_xlim(x_min, x_min + x_range)
    ax.set_ylim(y_min, y_min + y_range)
    ax.set_zlim(z_min, z_min + z_range)

    ax.set_xlabel("X (Longitude)")
    ax.set_ylabel("Y (Latitude)")
    ax.set_zlabel("T (Time)")

    ax.view_init(elev=elev, azim=azim)
    plt.tight_layout()

    return fig, ax

if __name__ == "__main__":
    rng = np.random.default_rng(42)
    n_points = 800

    XMAX, YMAX, ZMAX = 100, 100, 24
    x = rng.uniform(0, XMAX, n_points)
    y = rng.uniform(0, YMAX, n_points)
    z = rng.uniform(0, ZMAX, n_points)

    coords_example = np.column_stack([x, y, z])

    fig, ax = plot_3d_spatiotemporal(
        coords_example, optimal_scale=(20, 6), gap=0.075, cube_alpha=0.75
    )
    plt.show()
