from rest_framework import serializers
from logistic.models import Product, Stock, StockProduct


class ProductSerializer(serializers.ModelSerializer):
    # настройте сериализатор для продукта
    class Meta:
        model = Product
        fields = '__all__'


class ProductPositionSerializer(serializers.ModelSerializer):
    # настройте сериализатор для позиции продукта на складе
    class Meta:
        model = StockProduct
        fields = ['id', 'stock', 'product', 'quantity', 'price']
    product = serializers.PrimaryKeyRelatedField(queryset=Product.objects.all(),
                                                 required=True
                                                 )
    quantity = serializers.IntegerField(min_value=1, default=1)
    price = serializers.FloatField(min_value=1)


class StockSerializer(serializers.ModelSerializer):
    # настройте сериализатор для склада
    positions = ProductPositionSerializer(many=True)
    # positions = ProductPositionSerializer

    class Meta:
        model = Stock
        fields = '__all__'

    def create(self, validated_data):
        print('================')
        print(validated_data)
        # достаем связанные данные для других таблиц
        positions = validated_data.pop('positions')

        # создаем склад по его параметрам
        stock = super().create(validated_data)

        # здесь вам надо заполнить связанные таблицы
        # в нашем случае: таблицу StockProduct
        # с помощью списка positions
        for position in positions:
            StockProduct.objects.create(stock=stock,
                                        product=position['product'],
                                        quantity=position['quantity'],
                                        price=position['price'])
        return stock

    def update(self, instance, validated_data):
        # достаем связанные данные для других таблиц
        positions = validated_data.pop('positions')

        # обновляем склад по его параметрам
        stock = super().update(instance, validated_data)

        # здесь вам надо обновить связанные таблицы
        # в нашем случае: таблицу StockProduct
        # с помощью списка positions

        for position in positions:
            StockProduct.objects.update_or_create(stock=stock,
                                                  product=position['product'],
                                                  defaults={
                                                      'quantity': position['quantity'],
                                                      'price': position['price']})
        return stock
