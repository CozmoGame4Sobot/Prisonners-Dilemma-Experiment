import asyncio
import cozmo
import time
from cozmo.objects import LightCube1Id, LightCube2Id, LightCube3Id


async def log_cube_info(robot: cozmo.robot.Robot, cube_id):
    cube = robot.world.get_light_cube(cube_id)
    if cube is not None:
        cube.set_lights(cozmo.lights.red_light)
        time.sleep(2)
        # Wait for up to few seconds for the cube to have received battery level info
        for i in range(30):
            if cube.battery_voltage is None:
                if i == 0:
                    cozmo.logger.info("Cube %s waiting for battery info...", cube_id)
                await asyncio.sleep(0.5)
            else:
                break
        cozmo.logger.info("Cube %s battery = %s", cube_id, cube.battery_str)
    else:
        cozmo.logger.warning("Cube %s is not connected - check the battery.", cube_id)


async def cozmo_program(robot: cozmo.robot.Robot):
    await log_cube_info(robot, LightCube1Id)  # looks like a paperclip
    await log_cube_info(robot, LightCube2Id)  # looks like a lamp / heart
    await log_cube_info(robot, LightCube3Id)  # looks like the letters 'ab' over 'T'


cozmo.robot.Robot.drive_off_charger_on_connect = False
cozmo.run_program(cozmo_program)