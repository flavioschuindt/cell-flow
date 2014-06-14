from const import FRAME_PERIOD, INIT_WINDOW_SIZE, INIT_WINDOW_POSITION, \
    BACKGROUND_COLOR, TORUS_SIDES, TORUS_RINGS, TORUS_COLOR, \
    TORUS_INNER_RADIUS, TORUS_OUTTER_RADIUS, TORUS_MASS_RANGE, \
    TORUS_QUANTITY, FOVY, Z_NEAR, Z_FAR, FLUID_FORCE, GRAVITY_FORCE_FACTOR, \
    TORUS_DESIRED_SEPARATION, TORUS_FLOCKING_MAX_SPEED, TORUS_FLOCKING_MAX_FORCE, \
    GRID_CELL_QUANTITY, TORUS_LIMIT_X, TORUS_LIMIT_Y, TORUS_LIMIT_Z
from display.GenericObj import *
from torus import Torus
from vector import *
from grid import *

class ObjManager(object):
    def __init__(self):
        self.pool = []
        self.far_z = []
        self.z_values = []
        self.grid = None

    def create(self):
        for x in range(TORUS_QUANTITY):
            mass = random.uniform(*TORUS_MASS_RANGE)
            location_z = random.uniform(-TORUS_LIMIT_Z, TORUS_LIMIT_Z)
            self.z_values.append(location_z)
            location_x = random.uniform(-TORUS_LIMIT_X, TORUS_LIMIT_X)
            location_y = random.uniform(-TORUS_LIMIT_Y, TORUS_LIMIT_Y)
            t = Torus(
                sides=TORUS_SIDES,
                rings=TORUS_RINGS,
                color=TORUS_COLOR,
                location=(location_x, location_y, -1 * location_z),
                inner_radius=TORUS_INNER_RADIUS,
                outter_radius=TORUS_OUTTER_RADIUS,
                mass=mass,
                max_speed=TORUS_FLOCKING_MAX_SPEED,
                max_force=TORUS_FLOCKING_MAX_FORCE,
                # obj=GenericObj(size=TORUS_INNER_RADIUS + 2 * TORUS_OUTTER_RADIUS, model="hemacia.obj")
                obj=GenericObj(size=0.17, model="hemacia.obj")
            )
            self.pool.append(t)
        self.far_z = max(self.z_values)

    def update(self):
        global scene, grid
        fluid = PVector(*FLUID_FORCE)
        for index, torus in enumerate(self.pool):
            gravity = PVector(0, GRAVITY_FORCE_FACTOR * torus.mass)
            self.grid.remove(torus)
            torus.apply_force(fluid)
            torus.apply_force(gravity)
            torus.update()
            torus.flock(self.grid.get_neighbors(torus), TORUS_DESIRED_SEPARATION)
            torus.translate(torus.location.x, torus.location.y, torus.location.z)
            self.grid.insert(torus)
        # self.display()

    def display(self):
        for torus in self.pool:
            glMatrixMode(GL_MODELVIEW)
            # glLoadIdentity()

            glPushMatrix()
            glMultMatrixf(torus.matrix)
            # glRotate(45, 1, 0, 0)
            points = torus.calc_points() if len(torus.points) == 0 else torus.points
            torus.obj.display()
            glPopMatrix()

    def recreate_grid(self, l_x, l_y, cell_quantity):
        self.grid = Grid(
                width=l_x,
                height=l_y,
                cell_quantity=cell_quantity
                )



__author__ = 'bruno'
