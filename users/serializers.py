from djoser.serializers import UserDeleteSerializer


class CustomUserDeleteSerializer(UserDeleteSerializer):
	def destroy(self):
		# Hard delete
		self.instance.delete()
		return self.instance
