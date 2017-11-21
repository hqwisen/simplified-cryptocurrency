# from rest_framework.response import Response
# from rest_framework.views import APIView
#
# from common.models import Block
# from common.serializers import BlockSerializer
#
#
# class BlockchainView(APIView):
#     serializer_class = BlockSerializer
#     # TODO Build a pagination for part of blockchain request
#     # pagination_class = None
#
#
#     def post(self, request):
#         request.data
#         return Response({"This is a post answer"})
#     # def post(self, request):
#     #     data = request.data['data']['attributes']
#     #     print(data)
#     #     serializer = BlockSerializer(data=data)
#     #     valid = serializer.is_valid()
#     #     # block = BlockSerializer(request.data)
#     #     print(valid)
#     #     if valid:
#     #         block = serializer.save()
#     #     else:
#     #         print("Error not valid")
#     #     return Response("This is correct")
#     #
#     # def get(self, request):
#     #     block = Block(header="hash", nonce=5)
#     #     #serializer = BlockSerializer()
#     #     return Response(data=BlockSerializer(block).serialize(block))
#     #     # return Block.objects.all()
#     #
#     # # def create(self, request, *args, **kwargs):
#     # #     print(request.data)
#     # #    serializer = self.get_serializer(data=request.data)
#     # #    print(serializer.is_valid())
#     # #    return super(generics.ListCreateAPIView, self).create(request, args, kwargs)
#
#
# # import logging
# #
# # from rest_framework.response import Response
# # from rest_framework.views import APIView
# #
# # logger = logging.getLogger(__name__)
# #
# #
# #
# #
# # class TransactionView(APIView):
# #
# #     def post(self, request):
# #         # transaction = TransactionSerializer(request.data)
# #         return Response("Transaction POST")
# #
# #
# #     def get(self, request):
# #         # transaction = TransactionSerializer(request.data)
# #         return "Transaction GET"
# #
# #             #Relay.server.add_transaction(transaction)
# #
# # class RelayView(APIView):
# #
# #     def get(self, request):
# #         return Response("Hello from GET")
# #
# #     def post(self, request):
# #         return Response("Hello from POST")
# #
# # # class TransactionView(generics.ListAPIView):
# #  #   model_class = Transaction
# #   #  serializer_class = TransactionSerializer
# #    # pagination_class = None
# #
# #     #def get_queryset(self):
# # #       return Transaction.objects.all()
