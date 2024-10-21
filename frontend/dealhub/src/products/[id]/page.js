import React from 'react'
type Props= {
 params:{id:string}
}
const ProductDetails= async ({params:{id}}:Props)=>{
    const product= await getProductsById(id);
    if(!product)
        redirect('/')
   
export default ProductDetails;