<h1 align="center">Molecular schemes identificator</h1>
  
We made a website that finds `coordinates of the vertices`, `contour of the molecule` from photo that you upload. The project was completed in 2 days at the Hack.Genesis hackathon.

## Work process

1. Tracing the image to improve quality. To make it simplier, translating from a raster image to a vector.

<p align="center">
  <img width="700" align="center" src="https://sun9-49.userapi.com/c857020/v857020328/417ca/U17WFIzZa24.jpg" alt="1_step"/></p>
  
2. Using the Harris detector, we determine the coordinates of the vertices.

<p align="center">  
  <img width="700" align="center" src="https://sun9-35.userapi.com/c857020/v857020328/417d3/v8K6aVQTxnM.jpg" alt="2_step"/></p>
  
3. Create a dictionary of images and determine what vertices are letters.

<p align="center">  
  <img width="700" align="center" src="https://sun9-51.userapi.com/c857020/v857020328/417dc/KE6Z0HSZQO0.jpg" alt="3_step"/></p>
  
## Algorithm

[Click to see our calculations](https://github.com/evro23x/abstract_dog/blob/master/tonyStarkWorks/functions.ipynb)

## Opportunities for improvement

- Search letters using CNN
- Use bit mapping to speed up photo processing
- Reduce images to the same size to improve nodes detection

## Authors

[@Anthonyvol](https://github.com/Anthonyvol)
[@evro23x](https://github.com/evro23x)
[@elenaorlova](https://github.com/elenaorlova)
[@svaflica](https://github.com/svaflica)
[@lemarik](https://github.com/lemarik)
<p align="center">  
  <img width="700" align="center" src="https://sun9-62.userapi.com/c857020/v857020328/4185d/4GmNOcqUju0.jpg" alt="team"/></p>

---

_The project is made in python without the use of machine learning_
