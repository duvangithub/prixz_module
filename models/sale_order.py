from odoo import models, fields, api

class SaleOrder(models.Model):
    _inherit = 'sale.order'

    #Desarrollo de un Método en Odoo (Python)
    def action_confirm(self):
        #Sobreescribe la función action_confirm
        res = super(SaleOrder, self).action_confirm()
        #Agrega el template que se va a usar en el correo de la carpeta data
        template_id = self.env.ref('prixz_module.sale_confirmed_template').id
        for order in self:
            self.env['mail.template'].browse(template_id).send_mail(order.id, force_send=True)
        return res


    #Configuración de un Proceso Logístico

    """ 
    Tarea: Describe brevemente cómo configurarías y personalizarías el flujo de trabajo en Odoo para
    gestionar automáticamente el proceso de:
    1. Picking (selección de productos).
    2. Packing (empaquetado).
    3. Envío con integración con un sistema de paquetería (por ejemplo, DHL o FedEx).


    Solución
    1. Tener instalado el módulo de Inventarios
    2. Ir a Inventarios > Configuración y seleccionar la opción llamada "Ubicaciones de almacenamiento"
    3. Una vez seleccionada podemos crear en Inventario -> Configuración -> Ubicaciones las opciones de Almacenamiento y crear Ubicaciones especificas para el picking de productos.
    4. Para el packing vamos a Inventarios -> Configuración -> Activamos "Paquetes" esto activa las opciones de "Paquetes" en el submenuu de productos y "Tipos de paquetes" en el submenu de Configuración
    5. Para el envio con paqueteria Odoo ya nos trae los módulos de algunos como por ejemplo DHL, lo instalamos primero.
    6. Vamos a configuración y métodos de envio, se configura el método de DHL instalado y se selecciona en la opción de proveedor, despues de ponen sus credenciales para poder usarlo en la pestaña llamada Configuración DHL.

    """


    #Consulta SQL sobre Productos en Odoo
"""
    SELECT
    product_template.name AS product_name, -- Nombre del producto
    product_template.barcode AS barcode, -- Código de barras
    MAX(purchase_order.date_order) AS last_purchase_date, -- Última fecha de compra
    MAX(sale_order.date_order) AS last_sale_date -- Última fecha de venta
    FROM
        product_product
    JOIN
        product_template ON product_product.product_tmpl_id = product_template.id
    LEFT JOIN
        purchase_order_line ON product_product.id = purchase_order_line.product_id
    LEFT JOIN
        purchase_order ON purchase_order_line.order_id = purchase_order.id AND purchase_order.state IN ('purchase', 'done')
    LEFT JOIN
        sale_order_line ON product_product.id = sale_order_line.product_id
    LEFT JOIN
        sale_order ON sale_order_line.order_id = sale_order.id AND sale_order.state IN ('sale', 'done')
    GROUP BY
        product_template.name, product_template.barcode
    ORDER BY
        product_template.name;

"""
