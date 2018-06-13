import random
import arcade


# Main Game Class
class MyGame(arcade.Window):
    """ Called to run the game. """

    def __init__(self, width, height, title):

        # Call the parent class's init function
        super().__init__(width, height, title)
        arcade.set_background_color(arcade.color.BLACK)

        # All self.variables
        self.count = 0
        self.enemy_list = []
        self.target_selected = False
        self.health = 10
        self.enemies_dead = 0
        self.wave = 0
        self.enemies_killed = []
        self.dif = 0
        self.enemy_speed = 0.5
        self.hard_dif = 2
        self.easy_dif = 1

        # Creating all enemies
        enemy1 = Enemys("left", 50, 80, self.enemy_speed, 25, arcade.color.BLACK, True)
        self.enemy_list.append(enemy1)

        enemy2 = Enemys("left", 50, 240, self.enemy_speed, 25, arcade.color.BLACK, True)
        self.enemy_list.append(enemy2)

        enemy3 = Enemys("left", 50, 400, self.enemy_speed, 25, arcade.color.BLACK, True)
        self.enemy_list.append(enemy3)

        enemy4 = Enemys("left", 50, 560, self.enemy_speed, 25, arcade.color.BLACK, True)
        self.enemy_list.append(enemy4)

        enemy5 = Enemys("left", 50, 720, self.enemy_speed, 25, arcade.color.BLACK, True)
        self.enemy_list.append(enemy5)

        enemy6 = Enemys("right", 1350, 80, (self.enemy_speed * - 1), 25, arcade.color.BLACK, True)
        self.enemy_list.append(enemy6)

        enemy7 = Enemys("right", 1350, 240, (self.enemy_speed * - 1), 25, arcade.color.BLACK, True)
        self.enemy_list.append(enemy7)

        enemy8 = Enemys("right", 1350, 400, (self.enemy_speed * - 1), 25, arcade.color.BLACK, True)
        self.enemy_list.append(enemy8)

        enemy9 = Enemys("right", 1350, 560, (self.enemy_speed * - 1), 25, arcade.color.BLACK, True)
        self.enemy_list.append(enemy9)

        enemy10 = Enemys("right", 1350, 720, (self.enemy_speed * - 1), 25, arcade.color.BLACK, True)
        self.enemy_list.append(enemy10)

    def wave_manger(self):
        """ Called when all enemies die. """

        self.enemies_dead = 0
        self.wave += 1
        # Restets enemies and adds they enemies you have killed to a list
        for enemy in self.enemy_list:
            # checks if the wall or the player killed the enemy
            if max(enemy.health) == 0:
                # adds the dif to the enemies killed list
                self.enemies_killed.append(enemy.dif)

            # resets the enemy speed
            if enemy.left_right == "left":
                enemy.change_x = self.enemy_speed

            # resets the enemy speed
            elif enemy.left_right == "right":
                enemy.change_x = (self.enemy_speed * -1)

            # allows drawing of the enemy and updates
            enemy.life = True

        # gives the amount of easy and hard enemies
        x = (self.wave % 10)
        x += random.randint(-1, 1)
        hard_easy_list = list(range(0, 10))
        # hard list len() is how many hard enemies there will be
        hard_list = hard_easy_list[:x]
        # easy list len() is how many normal enemies there will be
        easy_list = hard_easy_list[x:]

        # changes the difficulty of the enemies to x enemies hard
        for number in hard_list:
            self.enemy_list[number].dif = self.hard_dif
            self.enemy_list[number].health_bars()

        # changes the difficult of the enemies to make x enemies normal
        for number in easy_list:
            self.enemy_list[number].dif = self.easy_dif
            self.enemy_list[number].health_bars()

        # every 10 waves it makes the hard normal and the hard even harder
        if (self.wave % 10) == 0:
            self.hard_dif += 1
            self.easy_dif += 1

    def draw_background(self):
        """ Called to draw the background. """
        arcade.draw_rectangle_filled((1400/2), (800/2), 1200, 800, arcade.color.ASH_GREY)
        arcade.draw_line(650, 800, 650, 0, arcade.color.BLACK, 10)
        arcade.draw_line(750, 800, 750, 0, arcade.color.BLACK, 10)
        # draws what wave round you are on
        arcade.draw_text(("Wave {}".format(self.wave)), 700, 785, arcade.color.RED, 14, width=200, align="center",
                         anchor_x = "center", anchor_y ="center")

    def on_draw(self):
        """ Called to draw the window. """

        arcade.start_render()

        # only draws if the player is alive
        if self.health != 0:
            # draws the background
            self.draw_background()
            # draws all enemies
            for enemy in self.enemy_list:
                enemy.draw()
            # draws circles representing health
            for person in range(1, (self.health + 1)):
                person_y = (((800 / self.health) * person) - ((800 / self.health) / 2))
                arcade.draw_circle_filled(700, person_y, 25, arcade.color.BLUE)

        # draws the lost screen
        else:
            self.lost()

    def lost(self):
        """ Called when player dies. """

        # prints text saying what wave you died on
        arcade.draw_text(("ALL IS LOST\n DIED ON WAVE {}".format((self.wave - 1))), 700, 775, arcade.color.RED, 14,
                         width=200, align="center", anchor_x="center", anchor_y="center")
        # prints text saying how many enemies you have killed
        arcade.draw_text(("YOU KILLED {} ROUGES".format(len(self.enemies_killed))), 700, 735, arcade.color.RED, 14,
                         width = 200, align = "center", anchor_x = "center", anchor_y = "center")
        # keeps count of what enemy the for loop is up too
        index = 1
        # draws a circle for every enemy killed
        for enemy in self.enemies_killed:
            # works out where to place circles
            x_place = ((1400 / len(self.enemies_killed)) * index) - (1400 / len(self.enemies_killed) / 2)
            arcade.draw_circle_filled(x_place, 400, 25, arcade.color.GRAY)
            # draws what difficulty the enemy was on the circle
            arcade.draw_text(str(enemy), x_place, 400, arcade.color.RED, 14, width=200, align="center",
                             anchor_x="center", anchor_y="center")
            # updates index
            index += 1

    def on_mouse_press(self, x, y, button, modifiers):
        """ Called when the user presses a mouse button. """

        # used for selecting enemies
        if button == arcade.MOUSE_BUTTON_LEFT:
            # only can select a new enemy is the previse enemy selected is dead
            if self.target_selected is False:
                # count value keeps track of what number the player is up to on the enemy health list
                self.count = 0
                # used for selecting the right side
                if x >= 625:
                    # top enemy
                    if 640 <= y <= 800:
                        self.target = self.enemy_list[9]
                        self.target_selected = True

                    if 480 <= y <= 640:
                        self.target = self.enemy_list[8]
                        self.target_selected = True

                    if 320 <= y <= 480:
                        self.target = self.enemy_list[7]
                        self.target_selected = True

                    if 160 <= y <= 320:
                        self.target = self.enemy_list[6]
                        self.target_selected = True

                    # bottom enemy
                    if 0 <= y <= 160:
                        self.target = self.enemy_list[5]
                        self.target_selected = True

                # used for selecting the right side
                elif x <= 775:
                    # top enemy
                    if 640 <= y <= 800:
                        self.target = self.enemy_list[4]
                        self.target_selected = True

                    if 480 <= y <= 640:
                        self.target = self.enemy_list[3]
                        self.target_selected = True

                    if 320 <= y < 480:
                        self.target = self.enemy_list[2]
                        self.target_selected = True

                    if 160 <= y <= 320:
                        self.target = self.enemy_list[1]
                        self.target_selected = True

                    # bottom enemy
                    if 0 <= y <= 160:
                        self.target = self.enemy_list[0]
                        self.target_selected = True

    def on_key_press(self, key, modifiers):
        """ Called when the user presses a key. """

        # checks if the key pressed matches the current enemy health target
        if self.target_selected is True:
            if self.target.health[self.count] == 1 and key == arcade.key.KEY_1:
                self.target.health[self.count] = 0
                self.count += 1

            elif self.target.health[self.count] == 2 and key == arcade.key.KEY_2:
                self.target.health[self.count] = 0
                self.count += 1

            elif self.target.health[self.count] == 3 and key == arcade.key.KEY_3:
                self.target.health[self.count] = 0
                self.count += 1

            elif self.target.health[self.count] == 4 and key == arcade.key.KEY_4:
                self.target.health[self.count] = 0
                self.count += 1

            elif self.target.health[self.count] == 5 and key == arcade.key.KEY_5:
                self.target.health[self.count] = 0
                self.count += 1

            elif self.target.health[self.count] == 6 and key == arcade.key.KEY_6:
                self.target.health[self.count] = 0
                self.count += 1

            elif self.target.health[self.count] == 7 and key == arcade.key.KEY_7:
                self.target.health[self.count] = 0
                self.count += 1

            elif self.target.health[self.count] == 8 and key == arcade.key.KEY_8:
                self.target.health[self.count] = 0
                self.count += 1

            elif self.target.health[self.count] == 9 and key == arcade.key.KEY_9:
                self.target.health[self.count] = 0
                self.count += 1

            if self.count == len(self.target.health):
                self.target_selected = False
                self.target.life = False
                self.enemies_dead += 1
                self.target.change_x = 0
                if self.target.left_right == "left":
                    self.target.position_x = 50
                else:
                    self.target.position_x = 1350

    def update(self, delta_time):
        """ Called to update our objects. Happens approximately 60 times per second."""

        # makes it so that self.health can not be a negative
        if self.health < 0:
            self.health = 0

        # only updates enemies and triggers wave manger if health is above 0
        if self.health != 0:
            for enemy in self.enemy_list:
                enemy.update()
            if self.enemies_dead == 10:
                self.wave_manger()
        else:
            pass


class Enemys:
    """ Maneges enemy variables. """

    def __init__(self, left_right, position_x, position_y, change_x, radius, color, life, dif=1):
        """ Creates all needed self.variables """
        self.left_right = left_right
        self.position_x = position_x
        self.position_y = position_y
        self.change_x = change_x
        self.radius = radius
        self.color = color
        self.life = life
        self.dif = dif
        self.health = []
        self.health_bars()

    def draw(self):
        """ Draws enemy circles. """
        arcade.draw_circle_filled(self.position_x, self.position_y, self.radius, self.color)
        arcade.draw_text(str(self.health), self.position_x, (self.position_y + 35), self.color, 14, width=200,
                         align="center", anchor_x="center", anchor_y="center")

    def update(self):
        """ updates enemy .life and position """
        if self.life is True:
            self.position_x += self.change_x

        # if enemy is past the wall this kills them and resets their position
        if self.left_right == "left" and self.position_x >= 625:
            self.change_x = 0
            self.position_x = 50
            self.life = False
            game.health -= 1
            game.enemies_dead += 1

        # if enemy is past the wall this kills them and resets their position
        if self.left_right == "right" and self.position_x <= 775:
            self.change_x = 0
            self.position_x = 1350
            self.life = False
            game.health -= 1
            game.enemies_dead += 1

        # if enemy was killed by player this updates .life
        if self.life is False:
            self.change_x = 0

    def health_bars(self):
        """ Called to create health bars for enemies. """

        """
        dif_1 = three number pattern
        dif_2 = three numbers
        dif_3 = 4 four number pattern
        dif_4 = 4 numbers
        dif_6-10 = 6-10 numbers
        """

        if self.dif == 1:
            numbers = [1, 2, 3]
            random.shuffle(numbers)
            numbers.pop(1)
            numbers3 = numbers.copy()
            numbers.pop(1)
            numbers = numbers3 + numbers
            self.health = numbers

        if self.dif == 2:
            numbers = [1, 2, 3]
            random.shuffle(numbers)
            self.health = numbers

        if self.dif == 3:
            numbers = [1, 2, 3, 4]
            random.shuffle(numbers)
            numbers.pop(1)
            numbers.pop(2)
            numbers2 = numbers.copy()
            numbers.reverse()
            numbers = numbers + numbers2
            self.health = numbers

        if self.dif == 4:
            numbers = [1, 2, 3, 4]
            random.shuffle(numbers)
            self.health = numbers

        if self.dif >= 6:
            numbers = list(range(1, self.dif))
            random.shuffle(numbers)
            self.health = numbers


""" Prints information players need to play the game. """
print("Click on a black circle to select it.\nPress the numbers above said circles to kill it, left to right.")
print("If the blacks circle makes it to your walls you lose 1 health for each.\nHealth is repented by your blue "
      "circles on the wall.\nThe less you have, the less dudes there are.")
ready = str(input("Ready? [Y/N] "))
if ready.title() == "Y":
    game = MyGame(1400, 800, "Rouge Warrior")
    arcade.run()
